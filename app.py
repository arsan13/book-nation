from flask import Flask, render_template, request, redirect
import pymongo
from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()
URI = os.getenv("MONGO_URI")

cluster = MongoClient(URI)
db = cluster["booksDb"]
collection = db["books"]

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def books():
    if request.method == 'POST':
        book_isbn = request.form['isbn']
        book_title = request.form['title']
        book_author = request.form['author']
        book_category = request.form['category']
        collection.insert_one({"isbn": book_isbn, "title": book_title,
                               "author": book_author, "category": book_category})
        return redirect('/')
    else:
        books = collection.find()
        return render_template('/index.html', books=books)


@app.route('/filter/<string:category>')
def filter_by_category(category):
    books = collection.find({"category": category})
    return render_template('index.html', books=books)


@app.route('/filter', methods=['GET', 'POST'])
def filter_by_author():
    if request.method == 'POST':
        book_author = request.form['author']
        books = collection.find({"author": book_author})
        return render_template('index.html', books=books)


@app.route('/delete/<string:isbn>')
def delete(isbn):
    collection.delete_one({"isbn": isbn})
    return redirect('/')


@app.route('/update/<string:isbn>', methods=['GET', 'POST'])
def update(isbn):

    book = collection.find_one({"isbn": isbn})

    if request.method == 'POST':
        book_title = request.form['title']
        book_author = request.form['author']
        book_category = request.form['category']
        collection.update_one({"isbn": isbn}, {"$set": {
                              "title": book_title, "author": book_author, "category": book_category}})
        return redirect('/')
    else:
        return render_template('/edit.html', book=book)


if __name__ == "__main__":
    app.run(debug=True)
