import os

from flask import Flask, render_template, request, redirect, url_for, session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
import requests
from flask import Response
import json
from flask_session import Session
from passlib.hash import sha256_crypt




app = Flask(__name__)

engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

#possible search methods
search_methods = ['isbn','title','author','year']

#This is the main route. If user eneters 127.0.0.1:5000, it will be routed to here and if user is already logged-in, we take him/her to search option page, otherwise ask him to login.

@app.route("/", methods=["GET", "POST"])
def index():
    """Main Page."""
    if request.method == "GET":
        if 'userid' in session.keys():
            return redirect(url_for("search_options"))
        else:
            return redirect(url_for("login"))
    else:
        return redirect(url_for("search_options"))

   
#This is the login route. When user login, we validate his credentials.
#if user is not registered yet, we take him to register page 
@app.route("/login", methods=["GET", "POST"])
def login():
   
    """User Login."""
    if request.method == "POST":
       usr = request.form.get("uname")
       psw = request.form.get("psw")
       db_usr = db.execute("SELECT * FROM USERS WHERE username = :uname", {"uname": usr}).fetchone()
       print(db_usr)
       if db_usr is None:
        return redirect("register")
       else:
        print(db_usr[0])
        print(sha256_crypt.verify(psw, db_usr[2]))
        if  (sha256_crypt.verify(psw, db_usr[2])) == True: 
           session['userid'] = db_usr[0]
           session['username'] = db_usr[1]
           return redirect(url_for("index"), code=307)
        else:
           return("Invalid user/pasword")
    else:
        if 'userid' in session.keys():
          return redirect(url_for("search_options"))
        else:
          return render_template("login.html", username=None)



#This is the logout route. When user logout, we take him to login screen again.
@app.route("/logout", methods=["GET","POST"])
def logout():
   """ User logout"""
   session.clear()
   return redirect(url_for("login"))






#This is the register route. When user try to login but does not have account yet, we take him/her to register page.
#or if user goes to regsiter link directly, we take him/her to here. 
@app.route("/register", methods=["GET", "POST"])
def register():

    """User Signup"""
    if request.method == "POST":
       usr = request.form.get("uname")
       psw = request.form.get("psw")
       psw_repeat = request.form.get("psw-repeat")
       if psw != psw_repeat:
         print("wrong input")
         return "Incorrect password"
       print("same password")
       print(usr)
       print(psw)
       psw = sha256_crypt.encrypt(psw)

       print(psw)

       if 'userid' in session.keys():
         if usr != session['userid']:
           return("You are already logged-in as: " +  session['username'])
       else:
         db_usr = db.execute("SELECT * FROM USERS WHERE username = :uname", {"uname": usr}).fetchone()
         if db_usr is None:
           db.execute("INSERT INTO USERS (username, password) VALUES(:uname, :psw)",{"uname": usr, "psw":psw})
           db.commit()
           db_usr = db.execute("SELECT * FROM USERS WHERE username = :uname", {"uname": usr}).fetchone()
           print(db_usr)
           if db_usr is None:
             return "registration failed"
       return redirect(url_for("login"))
    else:
        return render_template("register.html", username=None)


#search_option route
#user can search books using GET and POST method
#Incase of GET, user has to logged-in
@app.route("/search_options", methods=["GET", "POST"])
def search_options():
    if request.method == "GET":
        if 'userid' in session.keys():
          return render_template("search_options.html", search_options=search_methods, user=session['username'], username=session['username'])
        else:
          return redirect(url_for("login")) 
    else:
        return render_template("search_options.html", search_options=search_methods, user=session['username'], username=session['username'])



#booksearch route - The route is invoked when user submit the search method and search input 
@app.route("/booksearch", methods=["POST"])
def booksearch():
    """Search Book."""

    if 'userid' not in session.keys():
       return redirect(url_for("login")) 
    
    # Get form information.
    search_method = request.form.get("search_method")
    if search_method == None:
       return render_template("error.html", message="search method is missing", username=session['username']), 400

    try:
        search_input = request.form.get("search_input")
    except ValueError:
        return render_template("error.html", message="Invalid input.", username=session['username']), 400
    if search_method == 'year':
        query = "SELECT * FROM books WHERE " + search_method + " = " + search_input
    else:
        query = "SELECT * FROM books WHERE " + search_method + " LIKE '%" + search_input + "%'"

    #print (query)
    books = db.execute(query).fetchall()
    #print(books)
    if len(books) == 0:
       return render_template("error.html", message="book not found", username=session['username']), 400
    return render_template("books.html", books=books, username=session['username'])



#bookreview route - The route is invoked when user provides its rating for the book 
@app.route("/bookreview/<int:book_id>", methods=["POST"])
def bookreview(book_id):
    """Book Review."""

    if 'userid' not in session.keys():
       return redirect(url_for("login")) 

    # Get form information.
    try:
        rating = int(request.form.get("rating"))
    except:
        rating = 0

    if rating <= 0 or rating > 5:
        return ("please enter the rating between 1-5")

    review_comments = request.form.get("review_comments")

    #print (book_id,session['userid'],rating, review_comments) 

    exist = db.execute("SELECT count(*) from BOOKREVIEWS where book_id=:id AND user_id=:usr_id", {"id":book_id, "usr_id": session['userid']}).scalar()

    #print(exist)
    if exist == None or exist == 0:
        try:
            db.execute("INSERT INTO BOOKREVIEWS (book_id, user_id, rating, review) VALUES(:book_id, :user_id, :rating, :review)",{"book_id": book_id, "user_id":session['userid'], "rating": rating, "review": review_comments})
            db.commit()
            return Response("Thank You", status=200)
        except:
            return ("please enter the rating between 1-5")
    else:
        return("You have already reviewed the book")
    
#This route is invoked when user wants to retrive all the books when he is logged-in.  
@app.route("/books")
def books():
    """Lists all Books."""
    if 'userid' in session.keys():
      books  = db.execute("SELECT * FROM books").fetchall()
      if len(books) == 0:
         return render_template("error.html", message="books not found", username=session['username']), 404
      return render_template("books.html", books=books, username=session['username'])
    else:
       return redirect(url_for("login"))

#This route is invoked when user clicks on a specific book to retrive details about the book. Goodread reviews are extracted though RESTFULL API
@app.route("/books/<int:book_id>")
def book(book_id):
    """Lists details about a single book."""
    if 'userid' in session.keys():
       pass
    else:
       return redirect(url_for("login")) 

    # Make sure book exists.
    bk = db.execute("SELECT * FROM books WHERE id = :id", {"id": book_id}).fetchone()
    user_reviews = db.execute("select rating, review, username from bookreviews JOIN users ON users.id = bookreviews.user_id where book_id=:id",{"id":book_id});
    if bk is None:
        return render_template("error.html", message="No such Book.", username=session['username']), 404
    #print(bk['isbn'])
   
    try:
        res = requests.get("https://www.goodreads.com/book/review_counts.json", params={"key": "EW2zCYzA2gntELgIWExGw", "isbns": bk['isbn']})

        if res.status_code != 200:
          print("no review available")
          review_rating = "not available"
          review_cnt = 0
        book_review_dict = res.json()
        review_list = book_review_dict['books']
        review_dict = review_list[0]
        review_cnt = review_dict['work_reviews_count']
        review_rating = review_dict['average_rating']
        print (review_cnt, review_rating)
        #return 'bad render'
        return render_template("book.html", book=bk, user_reviews=user_reviews, review_cnt=review_cnt, review_rating=review_rating, username=session['username'])
    except:
        return render_template("error.html", message="goodread API has no review for this book", username=session['username']), 404

# this route is invoked when user wants to invoke API using ISBN
@app.route("/api/<book_isbn>")
def api(book_isbn):
    """Lists details about a single book."""
    if 'userid' in session.keys():
       pass
    else:
       return redirect(url_for("login")) 

    # Make sure book exists.
    bk = db.execute("SELECT * FROM books WHERE isbn = :id", {"id": book_isbn}).fetchone()
    if bk is None:
        return render_template("error.html", message="No such Book.", username=session['username']), 404
    #print(bk['id'])
    cavg = db.execute("select count(*), avg(rating) from bookreviews where book_id=:id",{"id":bk['id']}).fetchone()
    #print(cavg)
    if (cavg[1] == None) :
      book_dict = dict(title=bk['title'],author=bk['author'],year=bk['year'],isbn=bk['isbn'],review_count=cavg[0], avg_rating="") 
    else:
     book_dict = dict(title=bk['title'],author=bk['author'],year=bk['year'],isbn=bk['isbn'],review_count=cavg[0], avg_rating=float(cavg[1]))
   
    return Response(json.dumps(book_dict), status=200, mimetype="application/json")
