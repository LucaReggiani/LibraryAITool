from flask import Blueprint
from resources import BookList, Book

# Define routes
def setup_routes(api):
    api.add_resource(BookList, '/book_list')
    api.add_resource(Book, '/book_list/<book_id>')
