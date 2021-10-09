import csv
import os

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

engine = create_engine("postgres://postgres:password@localhost:5432/users")
db = scoped_session(sessionmaker(bind=engine))

def main():
    f = open("books.csv")
    reader = csv.reader(f)
    for isbn, title, author, year in reader:
        db.execute("INSERT INTO books (isbn, title, author, year) VALUES (:isbn, :title, :author, :year)",
                 {"isbn": isbn, "title": title, "author": author, "year": year})
        print(f"Book {title}  written by {author}")
    db.commit()

if __name__ == "__main__":
    main()
