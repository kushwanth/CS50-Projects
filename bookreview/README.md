# Book Review App with Goodreads API

## Dependencies used
- Flask
- Flask-Session
- psycopg2-binary
- SQLAlchemy
- requests

### About Project
- This project is my first python project.The code for importing books is in importbooks.py file and the rest of the code goes through appliction.py file
- this whole project and its databases are run under localhost on my computer so that I haven't added any sql files. 
- I have used 3 tables one for users, one for books and the last one for reviews.

### SETUP
- Clone repo
- Open repo folder after cloning

# Install all dependencies
$ pip install -r requirements.txt

# ENV Variables
$ export FLASK_APP = application.py
$ export DATABASE_URL = Your Database URI
$ flask run

# Go to 127.0.0.1:5000 on your web browser.

#### This is Project 1 for CS50's WEB PROGRAMMING USING PYTHON AND JAVASCRIPT
