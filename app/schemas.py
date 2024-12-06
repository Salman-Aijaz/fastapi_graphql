import strawberry
from typing import Optional

@strawberry.type
class Book:
    id: int
    name: str
    author: str
    quantity: int

@strawberry.input
class BookInput:
    name: str
    author: str
    quantity: int

    @strawberry.field
    def validate_quantity(self) -> None:
        if self.quantity < 0:
            raise ValueError("Quantity cannot be negative")

@strawberry.input
class BookUpdateInput:
    name: Optional[str] = None
    author: Optional[str] = None
    quantity: Optional[int] = None

    @strawberry.field
    def validate_quantity(self) -> None:
        if self.quantity is not None and self.quantity < 0:
            raise ValueError("Quantity cannot be negative") 