from sqlmodel import select
from database import get_db
from models import Book as BookModel
from schemas import BookInput, BookUpdateInput

# This file implements the repository pattern to interact with the database. 
# The idea is to separate the database logic from the business logic.

class BookRepository:

    @staticmethod
    async def get_all_books():
        async for session in get_db():
            result = await session.execute(select(BookModel))
            return result.scalars().all()

    @staticmethod
    async def get_book_by_id(book_id: int):
        async for session in get_db():
            statement = select(BookModel).where(BookModel.id == book_id)
            result = await session.execute(statement)
            return result.scalar_one_or_none()

    @staticmethod
    async def create_book(book_data: BookInput):
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

    @staticmethod
    async def update_book(book_id: int, book_data: BookUpdateInput):
        async for session in get_db():
            book = await BookRepository.get_book_by_id(book_id)
            if book is None:
                return None

            # Update fields if new data is provided
            if book_data.name is not None:
                book.name = book_data.name
            if book_data.author is not None:
                book.author = book_data.author
            if book_data.quantity is not None and book_data.quantity >= 0:
                book.quantity = book_data.quantity

            # No need to add book again as it's already in the session
            await session.commit()
            await session.refresh(book)  # Refresh to get updated data

            return book

    @staticmethod
    async def delete_book(book_id: int):
        async for session in get_db():
            book = await BookRepository.get_book_by_id(book_id)
            if book:
                await session.delete(book)
                await session.commit()
