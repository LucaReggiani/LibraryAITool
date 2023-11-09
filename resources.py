from flask_restful import reqparse, abort, Resource
from config import configuration
from models import BookModel
from flask import request
import json
from sqlalchemy import func

db = configuration.get_db()

BOOKS = {
    'book_1': {'title': '1984'}
}


def abort_if_todo_doesnt_exist(book_id):
    if book_id not in BOOKS:
        abort(404, message="Todo {} doesn't exist".format(book_id))

parser = reqparse.RequestParser()
parser.add_argument('title', required=True, type=str, help='The title is compulsory!', location='form')

# Single book retrieval
# shows a single book, allowing the user to edit it and to delete it
class Book(Resource):
    def get(self, book_id):
        abort_if_todo_doesnt_exist(book_id)
        return BOOKS[book_id]

    def delete(self, book_id):
        abort_if_todo_doesnt_exist(book_id)
        del BOOKS[book_id]
        return '', 204

    def put(self, book_id):
        args = parser.parse_args()
        book = {'title': args['title']}
        BOOKS[book_id] = book
        return book, 201


# BookList
# shows a list of all books, without any category
class BookList(Resource):
    def get(self):
        # Accessing the User table, assuming User has a title attribute
        
        '''
        query = db.session.query(BookModel.bookId, BookModel.title, BookModel.genres).filter(BookModel.rating >= 4.4)
        books = query.all()
        '''
        query = db.session.query(BookModel.title, BookModel.author, BookModel.coverImg, BookModel.rating, BookModel.price).limit(30)
        books = query.all()
        return [book._asdict() for book in books]


    def post(self):

        raw_data = request.get_data()
        data = json.loads(raw_data)

        # id book computation by taking last book id inserted
        last_book = db.session.query(BookModel).order_by(func.substr(BookModel.bookId, 6).cast(db.Integer).desc()).first()
        
        if last_book:
            last_book_id = last_book.bookId
        else:
            last_book_id = 'book_0'
        # new book id for the book added. This is the primary key
        new_book_id = f"book_{int(last_book_id.lstrip('book_')) + 1}"
        num_pages = data['pages'][0]
        if num_pages:
            num_pages = int(num_pages)
        else:
            num_pages = 0
        # Create a new Book instance and add it to the database
        new_book = BookModel(bookId=new_book_id, title=data['title'], series=data['series'], author=data['author'], rating=0,
                        description=data['description'], language=data['language'], genres=data['genres'],
                        pages=num_pages, publisher=data['publisher'], publishDate=data['publishDate'],
                        coverImg=data['coverImg'], price=data['price'])
        db.session.add(new_book)
        db.session.commit()
        
        return {'message': 'Book added successfully'}, 201