import os
import csv
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))

#class to create user table
#if table is already there, do nothing, else create Table
class users():
  def __init__(self, tab):
      self.createUsersTable(tab)
  #create users DB Table schema 
  def createUsersTable(self, tab):
       if not engine.dialect.has_table(engine, tab):
          query = 'CREATE TABLE ' + tab + '(id SERIAL PRIMARY KEY, username VARCHAR UNIQUE, password VARCHAR NOT NULL)'
          db.execute(query)
          db.commit()
          print(f"new table {tab} created")
       else:
          print(f"table exist: {tab}")
  #drop DB Table schema 
  def deleteUsersTable(self, tab):
          query = 'DROP TABLE if exists ' + tab
          db.execute(query)
          db.commit()


#class to create books table
#if table is already there,  then read books.csv file and insert each row if row does not exist in the table.

class books():
   def __init__(self, tab, booksinfo):
       self.createBooksTable(tab)
       self.insert(tab, booksinfo)

   #create DB Table schema 
   def createBooksTable(self, tab):
       if not engine.dialect.has_table(engine, tab):
          query = 'CREATE TABLE ' + tab + '(id SERIAL PRIMARY KEY, isbn VARCHAR UNIQUE, title VARCHAR NOT NULL, author VARCHAR NOT NULL, year INTEGER NOT NULL)'
          db.execute(query)
          db.commit()
          print(f"new table {tab} created")
       else:
          print(f"table exist: {tab}")


   #drop DB Table schema 
   def deleteBooksTable(self, tab):
          query = 'DROP TABLE if exists ' + tab
          db.execute(query)
          db.commit()

   #check if row already exist 
   def isRowExist (self, id, tab):
      query = "SELECT count(*) from " + tab + " where isbn=:isbn"
      return db.execute(query, {"isbn":id}).scalar()

   #insert Table entries from books.csv 
   def insert(self, tab, booksinfo):
      with open(booksinfo, newline='') as csvfile:
          reader = csv.DictReader(csvfile)
          for row in reader:
             if self.isRowExist(str(row['isbn']), tab) == 0:

                query = "INSERT INTO " + tab + "(isbn, title, author, year) VALUES(:isbn, :title, :author, :year)"
                db.execute(query, {"isbn": row['isbn'], "title": row['title'], "author":row['author'], "year":row['year']})
                print(f"Added book with isbn: {row['isbn']} title: {row['title']} author: {row['author']} year: {row['year']}")
             else:
                 print(f"row exist with isbn: {row['isbn']} title: {row['title']} author: {row['author']} year: {row['year']} ") 
          db.commit() 


#class to create review table

class reviews():
  def __init__(self, tab):
      self.createBookReviewTable(tab)
  #create book reviews DB Table schema 
  def createBookReviewTable(self, tab):
       if not engine.dialect.has_table(engine, tab):
          query = 'CREATE TABLE ' + tab + '(id SERIAL PRIMARY KEY, book_id INTEGER REFERENCES books, user_id INTEGER REFERENCES users, rating INTEGER CHECK (rating >= 1 AND rating <= 5), review VARCHAR)'
          db.execute(query)
          db.commit()
       else:
          print(f"table exist: {tab}")

  #drop DB Table schema 
  def deleteBookReviewTable(self, tab):
          query = 'DROP TABLE if exists ' + tab
          db.execute(query)
          db.commit()

#main table
if __name__ == "__main__":
    books('books', 'books.csv')
    users('users')
    reviews('bookreviews')
