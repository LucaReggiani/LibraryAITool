from sqlalchemy import Integer, String, Float
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
    language: Mapped[str] = mapped_column(String(5000), nullable=True)
    genres: Mapped[str] = mapped_column(String(5000), nullable=True)
    pages: Mapped[int] = mapped_column(Integer, nullable=True)
    publisher: Mapped[str] = mapped_column(String(715), nullable=True)
    publishDate: Mapped[str] = mapped_column(String(715), nullable=True)
    coverImg: Mapped[str] = mapped_column(String(715), nullable=True)
    price: Mapped[float] = mapped_column(Float, nullable=False)
