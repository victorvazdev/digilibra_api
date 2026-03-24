from sqlalchemy import Column, Integer, String, Float, Date, DateTime
from datetime import datetime, date
from typing import Union

from models.base import Base


class Book(Base):
    __tablename__ = 'book'

    id = Column('pk_book', Integer, primary_key=True)
    name = Column(String(100))
    author = Column(String(100))
    quantity = Column(Integer)
    value = Column(Float)
    release_date = Column(Date)
    insertion_date = Column(DateTime, default=datetime.now())

    def __init__(self, name:str, author:str, quantity:int, value:float, release_date:Date, insertion_date:Union[DateTime, None] = None):
        '''Cria um livro

        Argumentos:
            name: Nome do livro.
            author: Autor do livro.
            quantity: Quantidade disponível de livros.
            value: Preço do livro
            release_date: Data de lançamento do livro.
            insertion_date: Data de adição do livro na biblioteca.
        '''
        self.name = name
        self.author = author
        self.quantity = quantity
        self.value = value
        self.release_date = release_date

        # Caso a data de adição for informada, ela será configurada ao invés da data atual.
        if insertion_date:
            self.insertion_date = insertion_date
        
    # def update_book(self, book_updated):
    #     self.name = book_updated.name if book_updated.name is not None else self.name
    #     self.author = book_updated.author if book_updated.author is not None else self.author
    #     self.quantity = book_updated.quantity if book_updated.quantity is not None else self.quantity
    #     self.value = book_updated.value if book_updated.value is not None else self.value
    #     self.release_date = book_updated.release_date if book_updated.release_date is not None else self.release_date
