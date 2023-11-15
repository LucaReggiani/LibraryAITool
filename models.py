from sqlalchemy import Integer, String, Float, Boolean
from sqlalchemy.orm import Mapped, mapped_column
from config import configuration

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


class UserModel(db.Model):
    __tablename__ = 'User'

    userId: Mapped[str] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(55), nullable=False)
    lastname: Mapped[str] = mapped_column(String(55), nullable=False)
    email: Mapped[str] = mapped_column(String(55), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(500), nullable=False)
    is_admin: Mapped[bool] = mapped_column(Boolean, default=False)
