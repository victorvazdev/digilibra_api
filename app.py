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
    
    return display_book(book), 200

  
@app.delete('/book', tags=[book_tag], responses={'200': BookListSchema, '404': ErrorSchema})
def delete_book(query: BookDeleteSchema):
    session = Session()

    db_query = session.query(Book)
    db_query = db_query.filter(Book.id == query.id)
    book = db_query.first()
    book_deleted = db_query.delete()
    session.commit()

    if book_deleted:
        return {'message': f'Livro {book.name} de {book.author} foi removido com sucesso'}, 200
    else:
        return {'message': f'O livro de ID {query.id} não foi encontrado.'}, 404
    

@app.put('/update_book', tags=[book_tag], responses={'200': BookListSchema, '404': ErrorSchema})
def update_book(form: BookUpdateSchema):
    session = Session()

    db_query = session.query(Book)
    db_query = db_query.filter(Book.id == form.id)
    book = db_query.first()

    if not book:
        return {'message': f'O livro de ID {form.id} não foi encontrado.'}, 404
    
    # book.update_book(form)
    book.name = form.name if form.name is not None else book.name
    book.author = form.author if form.author is not None else book.author
    book.quantity = form.quantity if form.quantity is not None else book.quantity
    book.value = form.value if form.value is not None else book.value
    book.release_date = form.release_date if form.release_date is not None else book.release_date

    try:
        session.commit()
        return display_book(book), 200
    except Exception as e:
        return {'message': f'Erro ao atualizar: {str(e)}'}, 400