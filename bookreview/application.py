import os

from flask import Flask, session, render_template, request, redirect, url_for, flash, Response, jsonify
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from werkzeug.security import generate_password_hash, check_password_hash
from xml.dom.minidom import parse, parseString
import requests

app = Flask(__name__)
app.secret_key = 'cs50project1bykushwanth'

# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Set up database
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))

@app.route("/")
def index():
    return render_template("welcome.html")

@app.route("/signup")
def signup():
    return render_template("signup.html")

@app.route("/register", methods=["POST"])
def register():
#storing the information
       username = request.form.get("username")
       email = request.form.get("email")
       secure = request.form.get("password")
       pwd = generate_password_hash(secure)
       if db.execute("SELECT * FROM users WHERE username= :username", {"username":username}).rowcount >= 1:
          return render_template("error.html", message="UserName exist")
       db.execute("INSERT INTO users (username, email, password) VALUES (:username, :email, :secure)",
               {"username": username, "email": email, "secure": pwd})
       db.commit()
       return render_template("login.html")

@app.route("/signin")
def signin():
    return render_template("login.html")

@app.route("/login", methods=["POST"])
def login():
    username = request.form.get("username")
    access = request.form.get("password")
    auth = db.execute("SELECT * FROM users WHERE username= :uname", {"uname": username}).fetchone()
    assume = check_password_hash(auth.password, access)
    if (assume == True):
       session['loggedin'] = True
       session['username'] = request.form['username']
       return redirect(url_for('user'))
    return render_template('error.html', message='check your credentials')

@app.route("/user")
def user():
    if 'loggedin' in session:
       return render_template('user.html', user=session['username'])

@app.route("/user/search", methods=["GET", "POST"])
def search():
    if not 'loggedin' in session:
       return render_template('error.html', message= 'please login')
    search = request.form.get("search")
    res = requests.get('https://www.goodreads.com/search/index.xml', params= {"key": "OByurhy4Lzs93l1HdWn72w", "q": search, "page": "all"})
    result = parseString(res.content)
    head = result.getElementsByTagName('title')
    headman = result.getElementsByTagName('name')
    loop = result.getElementsByTagName('title').length
    data = {}
    for i in range(loop):
        bookname = head[i].firstChild.nodeValue
        authorname = headman[i].firstChild.nodeValue
        data.update({bookname: authorname})
    return render_template('books.html', data=data)

@app.route("/book", methods=["POST"])
def book():
    if not 'loggedin' in session:
       return render_template('error.html', message= 'please login')
    user = session['username']
    book = request.form.get("book")
    author = request.form.get("author")
    res = requests.get('https://www.goodreads.com/book/title.xml', params= {"author": author, "key": "OByurhy4Lzs93l1HdWn72w", "title": book})
    result = parseString(res.content)
    nameofbook = result.getElementsByTagName('title')[0].firstChild.nodeValue
    nameofauthor = result.getElementsByTagName('name')[0].firstChild.nodeValue
    year = result.getElementsByTagName('original_publication_year')[0].firstChild.nodeValue
    isbn = result.getElementsByTagName('isbn')[0].firstChild.nodeValue
    rating = result.getElementsByTagName('average_rating')[0].firstChild.nodeValue
    rate = result.getElementsByTagName('reviews_count')[0].firstChild.nodeValue
    if db.execute("SELECT title FROM reviews WHERE username= :username", {"username":user}).rowcount >= 1:
        view = db.execute("SELECT rating FROM reviews WHERE username= :username", {"username":user}).fetchone()
        return render_template('book.html', nameofbook=nameofbook, nameofauthor=nameofauthor, year=year, isbn=isbn, rating=rating, rate=rate, userview=view)
    return render_template('book.html', nameofbook=nameofbook, nameofauthor=nameofauthor, year=year, isbn=isbn, rating=rating, rate=rate)

@app.route("/book/submit", methods=["POST"])
def submit():
    user = session['username']
    booktitle = request.form.get("nameofbook")
    option = request.form.get("options")
    review = request.form.get("review")
    isbn = request.form.get("isbn")
    if db.execute("SELECT title FROM reviews WHERE username= :username", {"username":user}).rowcount >= 1:
          return render_template("error.html", message='review already exits')
    db.execute("INSERT INTO reviews (username, title, rating, reviewing, isbn) VALUES (:username, :title, :rating, :reviewing, :isbn)",
               {"username": user, "title": booktitle, "rating": option, "reviewing": review, "isbn": isbn})
    db.commit()
    return 'Review submitted successfully <a href="{{url_for("user/search")}}">search</a>'

@app.route("/api/<isbn>", methods=["GET"])
def api(isbn):
    apires = db.execute("SELECT * FROM books WHERE isbn=:isbn", {"isbn":isbn}).fetchone()
    totalview = db.execute("SELECT * FROM reviews WHERE isbn=:isbn", {"isbn":isbn}).rowcount
    userview = db.execute("SELECT rating FROM reviews WHERE isbn=:isbn", {"isbn":isbn}).fetchall()
    avg = 0
    for i in range(totalview):
        viewing = userview[i][0]
        avg+=viewing
    avgrating = float(avg/totalview)
    print(avgrating)
    apiresult = {"isbn": isbn, "title":apires.title, "author":apires.author, "year": apires.year, "review-count": totalview, "average-rating": avgrating}
    if isbn == "NULL":
        return render_template('error.html', message="isbn number doesn't exist")
    return jsonify(apiresult)

@app.route('/logout')
def logout():
   session.pop('loggedin', None)
   session.pop('username', None)
   return signin()
