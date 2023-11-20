from sqlalchemy import Column, Integer, String, Float, Boolean, Table
from sqlalchemy.orm import Mapped, mapped_column
from config import configuration
from sqlalchemy import ForeignKey
from typing import List
from sqlalchemy import Index
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base


db = configuration.get_db()

class BookModel(db.Model):
    __tablename__ = 'Book'

    bookId: Mapped[str] = mapped_column(String(715), primary_key=True)
    title: Mapped[str] = mapped_column(String(715), nullable=False)
    series: Mapped[str] = mapped_column(String(715), nullable=True)
    author: Mapped[str] = mapped_column(String(715), nullable=False)
    rating: Mapped[float] = mapped_column(Float, nullable=True)
    description: Mapped[str] = mapped_column(String(715), nullable=True)
    language_1: Mapped[str] = mapped_column(String(715), nullable=True)
    language_2: Mapped[str] = mapped_column(String(715), nullable=True)
    language_3: Mapped[str] = mapped_column(String(715), nullable=True)
    language_4: Mapped[str] = mapped_column(String(715), nullable=True)
    language_5: Mapped[str] = mapped_column(String(715), nullable=True)
    pages: Mapped[int] = mapped_column(Integer, nullable=True)
    publisher: Mapped[str] = mapped_column(String(715), nullable=True)
    publishDate: Mapped[str] = mapped_column(String(715), nullable=True)
    coverImg: Mapped[str] = mapped_column(String(715), nullable=True)
    price: Mapped[float] = mapped_column(Float, nullable=False)
    # Add an index on the bookId column
    __table_args__ = (Index('idx_bookId', 'bookId'),)
    reviews: Mapped[List["ReviewModel"]] = relationship(
         back_populates="book", cascade="all, delete-orphan"
    )
    cart: Mapped["CartItemsModel"]= relationship(
         back_populates="book", cascade="all, delete-orphan"
    )



class UserModel(db.Model):
    __tablename__ = 'User'

    userId: Mapped[str] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(55), nullable=False)
    lastname: Mapped[str] = mapped_column(String(55), nullable=False)
    email: Mapped[str] = mapped_column(String(55), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(500), nullable=False)
    is_admin: Mapped[bool] = mapped_column(Boolean, default=False)

    # Add an index on the userId column
    __table_args__ = (Index('idx_userId', 'userId'),)

    reviews: Mapped[List["ReviewModel"]] = relationship(
         back_populates="user", cascade="all, delete-orphan"
    )

    cart: Mapped["CartItemsModel"] = relationship(
         back_populates="user", cascade="all, delete-orphan"
    )


class ReviewModel(db.Model):
    __tablename__ = 'Review'

    reviewId: Mapped[str] = mapped_column(Integer, primary_key=True, autoincrement=True)
    rating: Mapped[float] = mapped_column(Float, nullable=False)
    review_description: Mapped[str] = mapped_column(String(1000))
    bookId: Mapped[str] = mapped_column(ForeignKey("Book.bookId"))
    userId: Mapped[str] = mapped_column(ForeignKey("User.userId"))

    book: Mapped["BookModel"] = relationship(back_populates="reviews")
    user: Mapped["UserModel"] = relationship(back_populates="reviews")


class CartItemsModel(db.Model):
    __tablename__ = 'Cart'

    cartId: Mapped[str] = mapped_column(Integer, primary_key=True, autoincrement=True)
    userId: Mapped[str] = mapped_column(ForeignKey("User.userId"))
    bookId: Mapped[str] = mapped_column(ForeignKey("Book.bookId"))
    quantity: Mapped[int] = mapped_column(Integer, nullable=True)
    total_price: Mapped[float] = mapped_column(Float, nullable=False)

    user: Mapped["UserModel"] = relationship(back_populates="cart")
    book: Mapped["BookModel"] = relationship(back_populates="cart")