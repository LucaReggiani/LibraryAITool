from resources import (BookList, 
                       Book, 
                       TranslationResource, 
                       FastTranslationResource, 
                       OrderBooksResource, 
                       BookFilteredList, 
                       UserRegistrationResource, 
                       UserLoginResource, 
                       BookReviews, 
                       AddToCart)

# Define routes
def setup_routes(api):
    api.add_resource(BookList, '/book_list')
    api.add_resource(OrderBooksResource, '/book_list/ordering')
    api.add_resource(Book, '/book_list/<book_id>')
    api.add_resource(BookFilteredList, '/filter_books')
    api.add_resource(BookReviews, '/reviews/<book_id>')
    api.add_resource(TranslationResource, '/translate')
    api.add_resource(FastTranslationResource, '/fast_translate')
    api.add_resource(UserRegistrationResource, '/signup')
    api.add_resource(UserLoginResource, '/login')
    api.add_resource(AddToCart, '/cart')
