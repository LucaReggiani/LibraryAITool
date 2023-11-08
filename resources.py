from flask_restful import reqparse, abort, Resource
from config import configuration
from models import BookModel

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
        
        query = db.session.query(BookModel.bookId, BookModel.title, BookModel.genres).filter(BookModel.rating >= 4.4)
        books = query.all()
        return [book._asdict() for book in books]


    def post(self):
        args = parser.parse_args()
        if not BOOKS:  # Check if BOOKS dictionary is empty
            book_id = 1
        else:
            book_id = int(max(BOOKS.keys()).lstrip('book_')) + 1
        book_id = 'book_%i' % book_id
        BOOKS[book_id] = {'title': args['title']}
        return BOOKS[book_id], 201