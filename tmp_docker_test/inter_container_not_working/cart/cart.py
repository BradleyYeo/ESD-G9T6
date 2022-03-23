from flask_sqlalchemy import SQLAlchemy
from flask import Flask, request, jsonify
from os import environ

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('dbURL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

#for week 4 lab
from flask_cors import CORS
db = SQLAlchemy(app)

#for week 4 lab
CORS(app)

class Book(db.Model):
    __tablename__ = 'book'

    isbn13 = db.Column(db.String(13), primary_key=True)
    title = db.Column(db.String(64), nullable=False)
    price = db.Column(db.Float(precision=2), nullable=False)
    availability = db.Column(db.Integer)

    def __init__(self, isbn13, title, price, availability):
        self.isbn13 = isbn13
        self.title = title
        self.price = price
        self.availability = availability

    def json(self):
        return {"isbn13": self.isbn13, "title": self.title, "price": self.price, "availability": self.availability}

@app.route("/book")
def get_all():
    booklist = Book.query.all()
    if len(booklist):
        return jsonify(
            {
                "code": 200,
                "data": {
                    "books": [book.json() for book in booklist]
                }
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "There are no books."
        }
    ), 404

@app.route("/book/<string:isbn13>")
def find_by_isbn13(isbn13):
    book = Book.query.filter_by(isbn13=isbn13).first()
    if book:
        return jsonify(
            {
                "code": 200,
                "data": book.json()
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "Book not found."
        }
    ), 404

#can also try put the isbn13 into the json and create book with @app.route("/book", methods=['POST'])

@app.route("/book/<string:isbn13>", methods=['POST'])
def create_book(isbn13):
    if (Book.query.filter_by(isbn13=isbn13).first()):
        return jsonify(
            {
                "code": 400,
                "data": {
                    "isbn13": isbn13
                },
                "message": "Book already exists."
            }
        ), 400

    data = request.get_json()
    book = Book(isbn13, **data) # **data expands the json into the init function

    try:
        db.session.add(book)
        db.session.commit()
    except:
        return jsonify(
            {
                "code": 500,
                "data": {
                    "isbn13": isbn13
                },
                "message": "An error occurred creating the book."
            }
        ), 500

    return jsonify(
        {
            "code": 201,
            "data": book.json()
        }
    ), 201

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
