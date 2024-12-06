import strawberry
from services import BookService
from schemas import BookInput, BookUpdateInput, Book

@strawberry.type
class Query:
    @strawberry.field
    async def books(self) -> list[Book]:
        return await BookService.get_books()

@strawberry.type
class Mutation:
    @strawberry.mutation
    async def create_book(self, book_data: BookInput) -> Book:
        return await BookService.create_book(book_data)

    @strawberry.mutation
    async def update_book(self, book_id: int, book_data: BookUpdateInput) -> Book:
        return await BookService.update_book(book_id, book_data)

    @strawberry.mutation
    async def delete_book(self, book_id: int) -> str:
        return await BookService.delete_book(book_id)

schema = strawberry.Schema(query=Query, mutation=Mutation)
