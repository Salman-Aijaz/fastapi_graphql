from sqlmodel import SQLModel, Field

class Book(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    name: str
    author: str
    quantity: int

    def __repr__(self):
        return f"Book(id={self.id}, name={self.name}, author={self.author}, quantity={self.quantity})"

class BookNotFoundError(Exception):
    pass

class InvalidBookDataError(Exception):
    pass