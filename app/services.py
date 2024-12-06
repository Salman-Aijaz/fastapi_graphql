from app.repository import BookRepository
from models import BookNotFoundError, InvalidBookDataError
from app.schemas import BookInput, BookUpdateInput, Book

class BookService:

    @staticmethod
    async def get_books() -> list[Book]:
        try:
            books = await BookRepository.get_all_books()
            return [Book(id=book.id, name=book.name, author=book.author, quantity=book.quantity) for book in books]
        except Exception as e:
            raise Exception(f"Error fetching books: {str(e)}")

    @staticmethod
    async def create_book(book_data: BookInput) -> Book:
        try:
            if book_data.quantity < 0:
                raise InvalidBookDataError("Quantity cannot be negative")
            new_book = await BookRepository.create_book(book_data)
            return Book(id=new_book.id, name=new_book.name, author=new_book.author, quantity=new_book.quantity)
        except InvalidBookDataError as e:
            raise e
        except Exception as e:
            raise Exception(f"Error creating book: {str(e)}")

    @staticmethod
    async def update_book(book_id: int, book_data: BookUpdateInput) -> Book:
        try:
            existing_book = await BookRepository.get_book_by_id(book_id)
            if not existing_book:
                raise BookNotFoundError(f"Book with id {book_id} not found")
            
            updated_book = await BookRepository.update_book(book_id, book_data)
            return Book(id=updated_book.id, name=updated_book.name, author=updated_book.author, quantity=updated_book.quantity)
        except BookNotFoundError as e:
            raise e
        except Exception as e:
            raise Exception(f"Error updating book: {str(e)}")

    @staticmethod
    async def delete_book(book_id: int) -> str:
        try:
            existing_book = await BookRepository.get_book_by_id(book_id)
            if not existing_book:
                raise BookNotFoundError(f"Book with id {book_id} not found")

            await BookRepository.delete_book(book_id)
            return f"Book with id {book_id} has been deleted"
        except BookNotFoundError as e:
            raise e
        except Exception as e:
            raise Exception(f"Error deleting book: {str(e)}")
