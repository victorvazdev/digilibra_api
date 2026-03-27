from sqlalchemy import Column, Integer, String, Float, Date, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from typing import Union

from models.base import Base


class Book(Base):
    '''Representa um livro no acervo da biblioteca.

    Esta entidade mapeia a tabela 'book' no banco de dados. Ela armazena os 
    detalhes comerciais, de estoque e de publicação da obra. Mantém um relacionamento 
    obrigatório de muitos-para-um (N:1) com a entidade Author através da chave 
    estrangeira 'author_id'.
    '''
    __tablename__ = 'book'

    id = Column('pk_book', Integer, primary_key=True)
    name = Column(String(100))
    author_id = Column(Integer, ForeignKey('author.id'), nullable=False)
    quantity = Column(Integer)
    value = Column(Float)
    release_date = Column(Date)
    insertion_date = Column(DateTime, default=datetime.now())
    author_rel = relationship('Author', back_populates='books')

    def __init__(self, name:str, author_id:int, quantity:int, value:float, release_date:Date, insertion_date:Union[DateTime, None] = None):
        '''Inicializa um novo registro de livro.

        Argumentos:
            name (str): Título do livro.
            author_id (int): Identificador (ID) do autor da obra já cadastrado no banco.
            quantity (int): Quantidade de exemplares disponíveis no acervo.
            value (float): Preço ou valor monetário do livro.
            release_date (Date): Data de lançamento ou publicação oficial da obra.
            insertion_date (DateTime, opcional): Data e hora em que o livro foi adicionado 
                ao sistema. Caso não seja informada, o sistema registrará o momento exato da criação.
        '''
        self.name = name
        self.author_id = author_id
        self.quantity = quantity
        self.value = value
        self.release_date = release_date

        # Caso a data de adição for informada, ela será configurada ao invés da data atual.
        if insertion_date:
            self.insertion_date = insertion_date            
