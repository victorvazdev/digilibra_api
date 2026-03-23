from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import date

from models.book import Book

class BookSchema(BaseModel):
    '''Define como um novo livro a ser inserido deve ser representado.
    '''
    name: str = Field('Clean Code')
    author: str = Field('Robert C. Martin')
    quantity: Optional[int] = Field(10)
    value: float = Field(289.6)
    release_date: Optional[date] = Field(default=date(2025, 10, 12))

class BookListSchema(BaseModel):
    books: List[BookSchema]

class BookSearchSchema(BaseModel):
    name: Optional[str] = Field('Clean Code', description='Nome do livro a ser buscado')
    author: Optional[str] = Field('Robert C. Martin', description='Nome do autor para busca precisa')

def display_book(book: Book):
    '''Retorna uma representação do livro seguindo o schema definido
    '''
    return {
        'id': book.id,
        'name': book.name,
        'author': book.author,
        'quantity': book.quantity,
        'value': book.value,
        'release_date': book.release_date
    }

def display_book_list(books: List[Book]):
    book_list = []

    for book in books:
        book_list.append({
            'id': book.id,
            'name': book.name,
            'author': book.author,
            'quantity': book.quantity,
            'value': book.value,
        '   release_date': book.release_date
        })

    return {'books': book_list}
