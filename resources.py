from flask_restful import reqparse, abort, Resource
from config import configuration
from models import BookModel, ReviewModel, UserModel, CartItemsModel
from flask import request
import json
from sqlalchemy import desc, func
from sqlalchemy.exc import SQLAlchemyError
from openai import OpenAI
import os
import asyncio
from openai import AsyncOpenAI
from dotenv import load_dotenv
import sys
from flask import make_response
from sqlalchemy import or_
from werkzeug.security import generate_password_hash, check_password_hash
from embeddings import *

load_dotenv()
api_key=os.getenv("OPENAI_KEY",None)

client = AsyncOpenAI(
    # defaults to os.environ.get("OPENAI_API_KEY")
    api_key=api_key,
)

clientSync = OpenAI(
    # defaults to os.environ.get("OPENAI_API_KEY")
    api_key=api_key,
)

db = configuration.get_db()

# Single book operations
# shows a single book, allowing the user to edit it and to delete it
class Book(Resource):
    def get(self, book_id):
        
        # Retrieve information about a specific book
            query = db.session.query(BookModel).filter_by(bookId=book_id)
            book = query.first()

            if book:
                main_book_dictionary = {
                    'bookId': book.bookId,
                    'title': book.title,
                    'series': book.series,
                    'author': book.author,
                    'rating': book.rating,
                    'description': book.description,
                    'language_1': book.language_1,
                    'language_2': book.language_2,
                    'language_3': book.language_3,
                    'language_4': book.language_4,
                    'language_5': book.language_5,
                    'pages': book.pages,
                    'publisher': book.publisher,
                    'publishDate': book.publishDate,
                    'coverImg': book.coverImg,
                    'price': book.price,
                }

                # adding the main book to a list
                books = [main_book_dictionary]

                # find suggested books using openai embeddings
                books_query = db.session.query(BookModel.bookId, BookModel.description).all()

                # Extracting bookId and description values into a list of tuple
                book_ids_description = [(book_id, description) for book_id, description in books_query]

                # suggested books
                suggested_book_ids = recommendations_from_descriptions(clientSync, main_book_dictionary, book_ids_description)
                if suggested_book_ids:
                    for recommended_book_id in suggested_book_ids:
                        recommended_book = db.session.query(BookModel).filter_by(bookId=recommended_book_id).first()

                        if recommended_book:
                            suggested_book_dictionary = {
                                'bookId': recommended_book.bookId,
                                'title': recommended_book.title,
                                'series': recommended_book.series,
                                'author': recommended_book.author,
                                'rating': recommended_book.rating,
                                'description': recommended_book.description,
                                'language_1': recommended_book.language_1,
                                'language_2': recommended_book.language_2,
                                'language_3': recommended_book.language_3,
                                'language_4': recommended_book.language_4,
                                'language_5': recommended_book.language_5,
                                'pages': recommended_book.pages,
                                'publisher': recommended_book.publisher,
                                'publishDate': recommended_book.publishDate,
                                'coverImg': recommended_book.coverImg,
                                'price': recommended_book.price,
                            }
                            books.append(suggested_book_dictionary)
                # books will be 1-element list if no description here is provided. 6 otherwise
                return books

            else:
                return {'error': 'Book not found'}, 404

    def delete(self, book_id):
        # Delete a specific book
        try:
            book = db.session.query(BookModel).filter_by(bookId=book_id).first()

            if book:
                db.session.delete(book)
                db.session.commit()
                return {'message': f'Book with ID {book_id} deleted successfully'}
            else:
                return {'error': 'Book not found'}, 404

        except SQLAlchemyError as e:
            db.session.rollback()
            return {'error': 'An error occurred while deleting the book'}, 500

    def put(self, book_id):
        raw_data = request.get_data()
        data = json.loads(raw_data)
        bookId = data.get('bookId')

        # Get the existing book from the database
        book = BookModel.query.get(bookId)

        # Update the book data with the new values
        book.title = data.get('title', book.title)
        book.series = data.get('series', book.series)
        book.author = data.get('author', book.author)
        book.rating = data.get('rating', book.rating)
        book.description = data.get('description', book.description)
        book.language_1 = data.get('language_1', book.language_1)
        book.language_2 = data.get('language_2', book.language_2)
        book.language_3 = data.get('language_3', book.language_3)
        book.language_4 = data.get('language_4', book.language_4)
        book.language_5 = data.get('language_5', book.language_5)
        book.pages = data.get('pages', book.pages)
        book.publisher = data.get('publisher', book.publisher)
        book.publishDate = data.get('publishDate', book.publishDate)
        book.coverImg = data.get('coverImg', book.coverImg)
        book.price = data.get('price', book.price)

        # Commit the changes to the database
        db.session.commit()

        return {'message': 'Book updated successfully'}, 200


# BookList
# shows a list of all books, without any category
class BookList(Resource):
    def get(self):
        # Accessing the User table, assuming User has a title attribute
        
        query = db.session.query(BookModel.bookId, BookModel.title, BookModel.author, BookModel.coverImg, BookModel.rating, BookModel.price)
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
        num_pages = data.get('pages')[0]
        if num_pages:
            num_pages = int(num_pages)
        else:
            num_pages = 0
        # Create a new Book instance and add it to the database
        new_book = BookModel(bookId=new_book_id, title=data['title'], series=data['series'], author=data['author'], rating=0,
                        description=data['description'], language_1=data['language_1'], language_2=data['language_2'], language_3=data['language_3'],
                        pages=num_pages, publisher=data['publisher'], publishDate=data['publishDate'],
                        language_4=data['language_4'], language_5=data['language_5'], coverImg=data['coverImg'], price=data['price'])
        db.session.add(new_book)
        db.session.commit()
        
        return {'message': 'Book added successfully'}, 201
    

class BookFilteredList(Resource):
    def post(self):
        raw_data = request.get_data()
        data = json.loads(raw_data)

        zero_filters = True

        title = data.get('title', '')[0]
        author = data.get('author', '')[0]
        language_1 = data.get('language_1', '')[0]
        language_2 = data.get('language_2', '')[0]
        language_3 = data.get('language_3', '')[0]
        language_4 = data.get('language_4', '')[0]
        language_5 = data.get('language_5', '')[0]
        price = data.get('price', '')[0]

        query_filtering = BookModel.query
        if title:
            query_filtering = query_filtering.filter(BookModel.title.ilike(f'%{title}%'))
            zero_filters = False
        if author:
            query_filtering = query_filtering.filter(BookModel.author.ilike(f'%{author}%'))
            zero_filters = False
        
        languages = [language_1, language_2, language_3, language_4, language_5]
        for language in languages:
            query_filtering = self.checkLanguages(language, query_filtering)
            zero_filters = False
        
        if price:
            query_filtering = query_filtering.filter(BookModel.price <= price)
            zero_filters = False
        
        if zero_filters:
            query_filtering = db.session.query(BookModel)

        books = query_filtering.all()

        result = []
        for book in books:
            book_dictionary = {
                    'bookId': book.bookId,
                    'title': book.title,
                    'author': book.author,
                    'rating': book.rating,
                    'coverImg': book.coverImg,
                    'price': book.price,
                }
            result.append(book_dictionary)
            
        return result
    
    @staticmethod
    def checkLanguages(language, query_filtering):
        if language:
            query_filtering = query_filtering.filter(or_(
                BookModel.language_1.ilike(f'%{language}%'),
                BookModel.language_2.ilike(f'%{language}%'),
                BookModel.language_3.ilike(f'%{language}%'),
                BookModel.language_4.ilike(f'%{language}%'),
                BookModel.language_5.ilike(f'%{language}%'),
            ))
        return query_filtering


class OrderBooksResource(Resource):
    def post(self):
        data = request.get_json()

        # Default to ordering by title if not provided
        order_by = data.get('order', 'title') 
        if order_by == 'price':
            books = db.session.query(BookModel).order_by(getattr(BookModel, order_by)).all()
        elif order_by == 'rating':
            books = db.session.query(BookModel).order_by(desc(getattr(BookModel, order_by))).all()
        else:
            books = db.session.query(BookModel.bookId, BookModel.title, BookModel.author, BookModel.coverImg, BookModel.rating, BookModel.price).all()

        # Serialize the books to a format suitable for the API response
        serialized_books = [
            {
                'bookId': book.bookId,
                'title': book.title,
                'author': book.author,
                'coverImg': book.coverImg,
                'rating': book.rating,
                'price': book.price,
            }
            for book in books
        ]

        return {'books': serialized_books}
    
class TranslationResource(Resource):

    def post(self):

        data = request.get_json()

        textsToTranslate = data.get('text', [])
        sourceLanguage = data.get('sourceLanguage', [])
        selectedLanguage = data.get('selectedLanguage', [])

        if not textsToTranslate:
            return {'error': 'Invalid input'}, 400
        
        return_dictionary = {}
        
        if selectedLanguage:
            ids = list(textsToTranslate.keys())
            texts = list(textsToTranslate.values())

            translation_texts = asyncio.run(self.translate_text(texts, sourceLanguage, selectedLanguage))

            return_dictionary = {ids[i]: translation_texts[i] for i in range(len(ids))}
        return return_dictionary

    def options(self):
        # Handle the preflight OPTIONS request
        response = make_response()
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
        response.headers.add('Access-Control-Allow-Methods', 'POST')
        return response

    @staticmethod
    async def translate_text(texts, source_language, target_language):
        example = "translations: [{'original': 'original_title', 'translated': 'translated_title'}, {'original': 'original_description', 'translated': 'translated_description'}]"
        prompt = f"You will be provided with a list of strings in {source_language}, and your task is to translate it into {target_language}. The output should be in JSON format. In detail, the given list will be made by several element, that can be one or more words per element. The output should be a JSON like this: {example}"

        response = await client.chat.completions.create(
            response_format={ "type": "json_object" },
            messages=[
                {"role": "system", "content": prompt},
                {"role": "user", "content": f"{texts}"}
            ],
            temperature=0,
            max_tokens=1000,
            model="gpt-3.5-turbo-1106",
        )

        translation = response.choices[0].message.content

        # Convert the JSON string to a dictionary
        json_response = json.loads(translation)
        json_response = json_response['translations']

        translations = []

        for item in json_response:
            translations.append(item['translated'])
            
        return translations
    


class FastTranslationResource(Resource):

    def post(self):

        data = request.get_json()

        textsToTranslate = data.get('text', [])
        sourceLanguage = data.get('sourceLanguage', [])
        selectedLanguage = data.get('selectedLanguage', [])

        if not textsToTranslate:
            return {'error': 'Invalid input'}, 400
        
        return_dictionary = {}

        if selectedLanguage:
            ids = list(textsToTranslate.keys())
            texts = list(textsToTranslate.values())

            fast_translation_texts = asyncio.run(self.fast_translate_text(texts, sourceLanguage, selectedLanguage))

            return_dictionary = {ids[i]: fast_translation_texts[i] for i in range(len(ids))}
        return return_dictionary

    def options(self):
        # Handle the preflight OPTIONS request
        response = make_response()
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
        response.headers.add('Access-Control-Allow-Methods', 'POST')
        return response

    @staticmethod
    async def fast_translate_text(texts, source_language, target_language):

        prompt = f"You will be provided with a list of strings in {source_language}, and your task is to translate it into {target_language}. The output should be in JSON format. In detail, the given list will be made by several element, that can be one or more words per element. The output should be one JSON with several items, one per list's element, translated. The given list of sentences is the following: {texts}"
        response = await client.completions.create(
            prompt=prompt,
            temperature=0,
            max_tokens=2000,
            model="text-davinci-003"
        )
        
        translation = response.choices[0].text
        json_response = json.loads(translation)
        translations = [item for item in json_response.values()]

        return translations
    

class UserRegistrationResource(Resource):
    def post(self):
        data = request.get_json()

        # Check if the username already exists
        if UserModel.query.filter_by(email=data['email']).first():
            return {'message': 'Username already exists'}, 400

        new_user = UserModel(email=data['email'], name=data['name'], lastname=data['lastname'], password=data['password'])
        db.session.add(new_user)
        db.session.commit()

        return {'message': 'User created successfully'}, 201


class UserLoginResource(Resource):
    def post(self):
        data = request.get_json()
        user = UserModel.query.filter_by(email=data['email']).first()
        password = data['password'][0]
        if user and check_password_hash(user.password, password):
            # Construct a dictionary with user details
            user_details = {
                'userId': user.userId,
                'name': user.name,
                'lastname': user.lastname,
                'email': user.email,
                'is_admin': user.is_admin
            }

            # Return the user details along with the success message
            return {'message': 'Login successful', 'user': user_details}, 200
        else:
            return {'message': 'Invalid credentials'}, 401
        

# ReviewList
class BookReviews(Resource):
    def get(self, book_id):
        # retrieving all the reviews of the current book, and relate author.
        reviews = (
            db.session.query(ReviewModel)
            .filter(ReviewModel.bookId == book_id)
            .join(UserModel, ReviewModel.userId == UserModel.userId)
            .all()
        )
        
        # Creating a list of dictionaries for each review
        reviews_data = []
        for review in reviews:
            review_data = {
                'reviewId': review.reviewId,
                'rating': review.rating,
                'review_description': review.review_description,
                'user_name': review.user.name,
                'user_lastname': review.user.lastname
            }
            reviews_data.append(review_data)

        return reviews_data


    def post(self, book_id):

        raw_data = request.get_data()
        data = json.loads(raw_data)
        bookId = book_id
        userId = data['userId']

        form_data = data['form_data']
        rating = form_data.get('rating', '')[0]
        review_description = form_data.get('review', '')[0]

        # Create a new review instance and add it to the database
        new_review = ReviewModel(rating=rating, review_description=review_description, bookId=bookId, userId=userId)
        db.session.add(new_review)
        db.session.commit()
        
        # recomputing average rating for the given book

        # sum of all the ratings
        sum_of_ratings = (
            db.session.query(func.sum(ReviewModel.rating))
            .filter(ReviewModel.bookId == book_id)
            .scalar() or 0
        )

        # counting all the reviews
        count_of_reviews = (
            db.session.query(func.count(ReviewModel.reviewId))
            .filter(ReviewModel.bookId == book_id)
            .scalar() or 0
        )

        average_rating = sum_of_ratings / count_of_reviews

        # Get the book instance
        book = db.session.query(BookModel).filter_by(bookId=book_id).first()

        # Check if the book exists
        if book:
            # Update the rating
            book.rating = average_rating

        # Commit the changes to the database
        db.session.commit()

        return "success!", 201
    

# ReviewList
class AddToCart(Resource):

    def get(self):

        raw_data = request.get_data()
        data = json.loads(raw_data)
        userId = data['userId']
        
        # retrieving all the books in the current user's cart
        cart_books = (
            db.session.query(CartItemsModel)
            .filter(CartItemsModel.userId == userId)
            .join(BookModel, CartItemsModel.bookId == BookModel.bookId)
            .all()
        )
        
        # Creating a list of dictionaries for each review
        cart_data = []
        for cart_book in cart_books:
            single_cart_data = {
                'cartId': cart_book.cartId,
                'userId': cart_book.userId,
                'bookId': cart_book.bookId,
                'quantity': cart_book.quantity,
                'total_price': cart_book.total_price,
                'title': cart_book.book.title,
                'author': cart_book.book.author,
                'rating': cart_book.book.rating,
                'price': cart_book.book.price,
                'coverImg': cart_book.book.coverImg,

            }
            cart_data.append(single_cart_data)

        return cart_data


    def post(self):

        raw_data = request.get_data()
        data = json.loads(raw_data)
        bookId = data['bookId']
        userId = data['userId']

        # checking if the current user already inserted the current book into the Cart
        result = db.session.query(CartItemsModel).filter(CartItemsModel.userId==userId, CartItemsModel.bookId==bookId).first()
        book_price = db.session.query(BookModel.price).filter(BookModel.bookId==bookId).first()[0]
        if result:
            result.quantity += 1
            result.total_price += book_price
        else:
            # Create a new Cart instance and add it to the database
            new_cart_item = CartItemsModel(quantity=1, total_price=book_price, bookId=bookId, userId=userId)
            db.session.add(new_cart_item)

        # Commit the changes to the database
        db.session.commit()

        return "success!", 201
    

    def options(self):
        # Handle the preflight OPTIONS request
        response = make_response()
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
        response.headers.add('Access-Control-Allow-Methods', 'POST')
        return response