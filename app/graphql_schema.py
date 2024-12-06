import strawberry
from app.services import BookService
from app.schemas import BookInput, BookUpdateInput, Book

@strawberry.type
class Query:
    @strawberry.field
    async def books(self) -> list[Book]:
        return await BookService.get_books()

@strawberry.type
class Mutation:
    @strawberry.mutation
    async def create_book(self, book_data: BookInput) -> Book:
        try:
            return await BookService.create_book(book_data)
        except Exception as e:
            return f"Error creating book: {str(e)}"

    @strawberry.mutation
    async def update_book(self, book_id: int, book_data: BookUpdateInput) -> Book:
        try:
            return await BookService.update_book(book_id, book_data)
        except Exception as e:
            return f"Error updating book: {str(e)}"

    @strawberry.mutation
    async def delete_book(self, book_id: int) -> str:
        try:
            return await BookService.delete_book(book_id)
        except Exception as e:
            return f"Error deleting book: {str(e)}"

schema = strawberry.Schema(query=Query, mutation=Mutation)
