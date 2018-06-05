# Project 1

Web Programming with Python and JavaScript


This project is to develop a book review website. The main focus on this project is to make sure the sitelooks realistic in terms of functionality and user experience. I have not focused on look and feel of the website. I implemented the site in such a way that user can not access site database info w/o first logged-in the system. Everytime user try to enter into the site by other means, he/she will asked to log-in first if he/she has not logged-in yet.


When user types 127.0.0.01:5000, my website should take the user to login page. I should also provide an option for the user to register if he has not created the account yet. if user is already logged-in, I should directly take him/her to search page.

Also, my website will have navbar where it display's my website name and if user is logged-in, it will display his/her name on the navbar and a logout button to provide the user option to logout anytime from any page.

If user is not logged-in yet, user name will not be displayed and a login button will be shown.

The navbar and dynamic info about user and its login status in navbar are  implemented in common layout.html file.

password is saved asfter SHA256 hash. So, password will not be in clear text. I used passlib module to do that.

My project has the following artifacts:
1. import.py:
   This file creates 3 tables using 3 classes one for each table and I create 5000 rows to load the book details in books table.
   The tables are - books, users, bookreviews.

   The books table have book info.
   The users table have user id and password.
   The bookreviews table has book review details - which book reviewed by which user. The table has foreign references to books table as well as users table. 

   Here is the schema:

    CREATE TABLE books (
    id SERIAL PRIMARY KEY,
    isbn VARCHAR  UNIQUE,
    title VARCHAR NOT NULL,
    author VARCHAR NOT NULL,
    year INTEGER  NOT NULL
    );

    CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR UNIQUE,
    password VARCHAR NOT NULL);

    CREATE TABLE bookreviews (
    id SERIAL PRIMARY KEY,
    book_id INTEGER REFERENCES books,
    user_id INTEGER REFERENCES users,
    rating  INTEGER CHECK (rating > 0 AND RATING <= 5),
    review  VARCHAR);
   


1. Application.py - Flask basedd python code to routed. I have created 4 search options for the user to serach the book. The file is self explanatory as it has proper comments.
2. All the html files are under template folder.

   The following html files are there:
    layout.html: This has navbar and it creates username and login/logout button in navbar depending on user's login status.
    login.html - to display login form. This will also display register button.
    register.html - to display regsiter form. 
    search_options.html - To provide user with  options to search the book.
    books.html - To provide user with list of books 
    book.html -to provide user with the details of a specific info including goodread.com ratings and form to ask user to review the book.
    error.html - to display erro message

    
3. CSS for the website is stored in static/css.

4. Extra modules needed:  jason, passlib
