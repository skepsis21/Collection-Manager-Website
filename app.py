import os
from math import *

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required

# Configure application
app = Flask(__name__)


# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
if not os.path.exists("collection.db"):
    from init_db import init_db
    init_db()

db = SQL("sqlite:///collection.db")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
def index():

    return render_template("index.html")


@app.route("/rate", methods=["GET", "POST"])
@login_required
def rate():
    # ADD SESSION FOR USER
    # GET input from user
    if request.method == "POST":
        name = request.form.get("name")
        strategy = request.form.get("strategy", "0")
        theme = request.form.get("theme", "0")
        ease = request.form.get("ease", "0")
        replay = request.form.get("replay", "0")
        length = request.form.get("length", "0")
        aesthetics = request.form.get("aesthetics", "0")
        interaction = request.form.get("interaction", "0")
        best = request.form.get("best", "0")
        fun = request.form.get("fun", "0")

        ratings = [strategy, theme, ease, replay, length, aesthetics, interaction, best, fun]

        # Check for errors
        if not name:
            return apology("Provide a board game")
        for rating in ratings:
            if not rating:
                return apology("All rating fields are required")
            try:
                value = int(rating)
                if not 1 <= value <= 5:
                    return apology("Ratings must be in range (1-5)")
            except ValueError:
                return apology("Provide valid numbers")

        # 1. Calculate points with updated weights (Total maximum weight = 22)
        total_points = (
            (int(fun) * 9) + 
            (int(strategy) * 4) + 
            (int(theme) * 4) + 
            (int(ease) + int(replay) + int(length) + int(aesthetics) + int(interaction))
        )

        # 2. Divide by 22 to map perfectly onto a 1.0 to 5.0 scale
        score = round(total_points / 22, 1)

        # Player ID
        player_id = session["user_id"]
        
        # Insert new game into database
        db.execute("INSERT INTO collection (name, strategy, theme, ease, replay, length, aesthetics, interaction, best, fun, score, player_id) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", name, strategy, theme, ease, replay, length, aesthetics, interaction, best, fun, score, player_id)

        return redirect("/rate")

    return render_template("/rate.html")


@app.route("/collection", methods=["GET"])
@login_required
def collection():
    """Show collection with dynamic column sorting"""
    
    # 1. Capture the sort criteria from the URL parameter (defaulting to score if none provided)
    sort_by = request.args.get("sort", "score")
    
    # 2. Whitelist valid database columns to protect against SQL Injection
    valid_sorts = {
        "strategy": "strategy DESC, score DESC",
        "theme": "theme DESC, score DESC",
        "best": "best DESC, score DESC",
        "score": "score DESC",
        "name": "name ASC"
    }
    
    # If the user provides an invalid sort parameter, fallback safely to sorting by score
    order_clause = valid_sorts.get(sort_by, "score DESC")
    
    # 3. Inject the dynamic order clause safely into the query execution block
    query = f"SELECT id, name, strategy, theme, ease, replay, length, aesthetics, interaction, best, fun, score FROM collection WHERE player_id = ? ORDER BY {order_clause}"
    games = db.execute(query, session["user_id"])

    # 4. Pass the active sort type back to the template so we can highlight it if wanted
    return render_template("/collection.html", games=games, active_sort=sort_by)

@app.route("/remove", methods=["POST"])
@login_required
def remove():
    """Remove a game from collection"""
    game_id = request.form.get("game_id")

    # Check for game_id
    if not game_id:
        return redirect("/collection")

    db.execute("DELETE FROM collection WHERE id = ? AND player_id = ?", game_id, session["user_id"])

    return redirect("/collection")
@app.route("/notes/<int:game_id>", methods=["GET", "POST"])
@login_required
def notes(game_id):
    """View and edit notes for a specific game"""

    # Verify the game belongs to the user
    game = db.execute("SELECT id, name, notes FROM collection WHERE id = ? AND player_id = ?", game_id, session["user_id"])
    if not game:
        return redirect("/collection")
    if request.method == "POST":
        note_content = request.form.get("notes")

        # Update notes in database
        db.execute("UPDATE collection SET notes = ? WHERE id = ? AND player_id = ?", note_content, game_id, session["user_id"])
        return redirect("/collection")

    return render_template("notes.html", game=game[0])


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        if not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute(
            "SELECT * FROM users WHERE username = ?", request.form.get("username")
        )

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(
            rows[0]["hash"], request.form.get("password")
        ):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    session.clear()

    if request.method == "POST":

        # Validate
        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        # Create database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", username)

        # Check password
        if not username:
            return apology("Username required")
        if not password:
            return apology("Password required")
        if not confirmation:
            return apology("Must confirm password")
        if password != confirmation:
            return apology("Password doesn't match")
        if len(rows) == 1:
            return apology("Username already exists")
        else:
            hashcode = generate_password_hash(password)
            db.execute("INSERT INTO users (username, hash) VALUES(?, ?)", username, hashcode)

        return redirect("/")
    else:
        return render_template("register.html")

@app.route("/about")
def about():

    return render_template("/about.html")
