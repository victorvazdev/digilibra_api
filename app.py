from flask_openapi3 import OpenAPI, Info, Tag
from flask import redirect
from sqlalchemy.exc import IntegrityError

from schemas.book_schema import *
from schemas.error_schema import ErrorSchema
from models.book import Book
from models import Session

# Definindo infomações básicas.
info = Info(title='Digilibra', version='1.0.0')
app = OpenAPI(__name__, info=info)

# Definindo tags.
book_tag = Tag(name='Book', description='Gerenciamento de livros')


@app.get('/')
def home():
    return redirect('/openapi')

@app.post('/book', tags=[book_tag], responses={'200': BookSchema, '400': ErrorSchema})
def add_book(form: BookSchema):
    '''Adiciona um novo livro e retorna uma apresentação do livro.
    '''
    book = Book(
        name=form.name,
        author=form.author,
        quantity=form.quantity,
        value=form.value,
        release_date=form.release_date
    )

    try:
        session = Session()
        session.add(book)
        session.commit()
        return display_book(book), 200
    except IntegrityError as e:
        return {'message': f'Erro ao adicionar o livro {book.name}: {e}'}, 409
    except Exception as e:
        return {'message': str(e)}, 400


@app.get('/books', tags=[book_tag], responses={'200': BookListSchema, '404': ErrorSchema})
def get_books():
    session = Session()
    books = session.query(Book).all()

    if not books:
        return {'books': []}, 200
    else:
        return display_book_list(books), 200
    
@app.get('/book', tags=[book_tag], responses={'200': BookListSchema, '404': ErrorSchema})
def get_book(query: BookSearchSchema):
    session = Session()

    db_query = session.query(Book)

    if query.name:
        db_query = db_query.filter(Book.name == query.name)

    if query.author:
        db_query = db_query.filter(Book.author == query.author)

    book = db_query.first()

    if not book:
        return {'message': 'O livro não foi encontrado.'}, 404
    else :
        return display_book(book), 200