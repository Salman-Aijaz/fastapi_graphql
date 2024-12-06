from sqlmodel import select
from database import get_db
from models import Book as BookModel, BookNotFoundError
from app.schemas import BookInput, BookUpdateInput
from sqlalchemy.exc import SQLAlchemyError
import logging

logger = logging.getLogger(__name__)

# This file implements the repository pattern to interact with the database. 
# The idea is to separate the database logic from the business logic.

class BookRepository:

    @staticmethod
    async def get_all_books():
        try:
            async for session in get_db():
                result = await session.execute(select(BookModel))
                return result.scalars().all()
        except SQLAlchemyError as e:
            logger.error(f"Database error while fetching all books: {str(e)}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error while fetching all books: {str(e)}")
            raise

    @staticmethod
    async def get_book_by_id(book_id: int):
        try:
            async for session in get_db():
                statement = select(BookModel).where(BookModel.id == book_id)
                result = await session.execute(statement)
                return result.scalar_one_or_none()
        except SQLAlchemyError as e:
            logger.error(f"Database error while fetching book {book_id}: {str(e)}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error while fetching book {book_id}: {str(e)}")
            raise

    @staticmethod
    async def create_book(book_data: BookInput):
        try:
            async for session in get_db():
                new_book = BookModel(
                    name=book_data.name,
                    author=book_data.author,
                    quantity=book_data.quantity
                )
                session.add(new_book)
                await session.commit()
                await session.refresh(new_book)
                return new_book
        except SQLAlchemyError as e:
            logger.error(f"Database error while creating book: {str(e)}")
            await session.rollback()
            raise
        except Exception as e:
            logger.error(f"Unexpected error while creating book: {str(e)}")
            raise

    @staticmethod
    async def update_book(book_id: int, book_data: BookUpdateInput):
        try:
            async for session in get_db():
                statement = select(BookModel).where(BookModel.id == book_id)
                result = await session.execute(statement)
                book = result.scalar_one_or_none()

                if book is None:
                    raise BookNotFoundError(f"Book with id {book_id} not found")

                if book_data.name is not None:
                    book.name = book_data.name
                if book_data.author is not None:
                    book.author = book_data.author
                if book_data.quantity is not None and book_data.quantity >= 0:
                    book.quantity = book_data.quantity

                await session.commit()
                await session.refresh(book)
                return book
        except SQLAlchemyError as e:
            logger.error(f"Database error while updating book {book_id}: {str(e)}")
            await session.rollback()
            raise
        except BookNotFoundError:
            raise
        except Exception as e:
            logger.error(f"Unexpected error while updating book {book_id}: {str(e)}")
            raise

    @staticmethod
    async def delete_book(book_id: int):
        try:
            async for session in get_db():
                statement = select(BookModel).where(BookModel.id == book_id)
                result = await session.execute(statement)
                book = result.scalar_one_or_none()

                if book is None:
                    raise BookNotFoundError(f"Book with id {book_id} not found")

                await session.delete(book)
                await session.commit()
        except SQLAlchemyError as e:
            logger.error(f"Database error while deleting book {book_id}: {str(e)}")
            await session.rollback()
            raise
        except BookNotFoundError:
            raise
        except Exception as e:
            logger.error(f"Unexpected error while deleting book {book_id}: {str(e)}")
            raise