PS C:\Users\User\Code_Space> .\.venv\Scripts\activate
(.venv) PS C:\Users\User\Code_Space\CS50_Final\skepsis21> flask run

### Roll And Rate - a board game collection manager ###

## Video Demo:  <(https://youtu.be/Ymjg76LFuVQ)>

# Author of the project #
Georgi Iliev Georgiev - https://github.com/skepsis21 - https://profile.edx.org/u/George050

### Description:

Roll And Rate is a web based application for rating and managing a board game collections with a focus on intuitive user experience and advanced, weighted ranking functionalities. By combining robust user authentication, a customizable rating interface, detailed note-taking, and a dynamic collection dashboard, the platform empowers users to curate, evaluate, and revisit their favorite games with ease. At the heart of the application lies a sophisticated weighted ranking tool, allowing users to score board games across multiple criteria, with the final ranking reflecting the true essence of each game according to user-defined priorities. The clean, responsive user interface ensures effortless navigation and interaction throughout every step of the process.

### Core Features

### 1. User Authentication and Security
- Registration & Login: New users can register by choosing a unique username and password, with password confirmation to avoid errors. Existing users log in via a secure form, leveraging password hashing for protection.
- Session Management: User sessions are securely managed using server-side sessions, ensuring personal collections and ratings remain private and persistent throughout the user’s visit.
- Logout: With a single click, users can safely end their session, guaranteeing account security.

### 2. Weighted Ranking Tool
- Multi-Criteria Rating: When adding or rating a game, users evaluate across several attributes: strategy, theme, ease of play, replayability, length, aesthetics, interaction, “best” factor, and fun.
- Custom Weighting Formula: The application does not simply average scores. Instead, it calculates a weighted score:
    - *Fun* is heavily weighted (multiplied by 4), emphasizing the core enjoyment factor.
    - *Strategy*, *theme*, and *ease* are moderately weighted (each multiplied by 3), reflecting their substantial impact.
    - Other attributes (replay, length, aesthetics, interaction, best) contribute to the base score.
    - The result is normalized and rounded for clarity.
- Ranking and Sorting: Each game in a user’s collection is automatically ranked by its weighted score, allowing users to instantly see their top-rated games according to what matters most to them.
- Validation and Error Handling: The system ensures all required ratings are provided, are within the valid range, and are numerically correct, minimizing user input errors.

### 3. Game Collection Management
- Add & Rate Games: Users seamlessly add new games to their collection, entering names and scores in a user-friendly form.
- View Collection: A dedicated collection page displays all games, sorted by the weighted score. Each entry shows detailed breakdowns of individual ratings, making it easy to compare games at a glance.
- Remove Games: Users can swiftly remove games from their collection with a single action, maintaining a curated and up-to-date list.

### 4. Notes and Reviews
- Per-Game Notes: For each game, users can write, edit, and save personal notes—perfect for recording impressions, house rules, or session recaps. Notes are private and easily accessible from the collection view.

### 5. User Interface and Experience
- Clean, Responsive Design: The application uses Flask’s templating system to deliver an uncluttered, modern interface that works smoothly on desktop and mobile devices.
- Clear Navigation: The navigation bar provides direct access to all major sections: Home, Add/Rate Game, Collection, Notes, About, Login/Logout, and Register.
- Real-Time Feedback: Friendly error messages and confirmations ensure users are always aware of the outcome of their actions—whether adding a game, saving a note, or encountering input errors.
- Usability Focus: Forms are simple, with logical field order and clear labels. All interactive elements respond promptly, and the collection table is easy to scan and interpret.

### 6. Additional Features
- About Page: A static page offers users information about the application, its purpose, and usage instructions.
- Performance and Security: HTTP headers are set to prevent unwanted caching, ensuring users always view the latest data while keeping personal information secure.

This combination of advanced scoring algorithms, robust account management, and an ergonomic interface makes the application a powerful ally for anyone passionate about board games and collection management.


Build with:

  Flask - web framework
  Python 3 - programming language
  HTML5 - markup language
  CSS - style sheet language
  Bootstrap - CSS framework
  SQL - query language for data manipulation
  CS50 - CS50s Library for Python

Reference:

  cdn.cs50.net/
  knowyourmeme.com/
  replit.com/
  programiz.com/
  w3schools.com/
  getbootstrap.com/

requirements to run FLASK AND CS50

python3 -m venv venv
source venv/bin/activate
pip install flask
pip install --upgrade pip
pip install flask cs50 flask-session requests