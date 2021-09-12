import base64
from werkzeug.utils import secure_filename
from schema import Schema, SchemaError, And, Use
from flask import request, jsonify, current_app
from flask_jwt_extended import current_user, jwt_required
from app import db
from app.api import bp
from app.api.errors import bad_request, forbidden, not_found
from app.models import Book, BookGenre, Genre, Review
from app.schemas import BookSchema, ReviewSchema
from app.utils import validate_date


@bp.route('/books', methods=['POST'])
@jwt_required()
def book_creation():
    if not current_user.is_author:
        return forbidden('User is not an author.')

    title = request.form['title']
    description = request.form['description']
    cover = request.files['cover']

    if not title or not description or not cover:
        return bad_request('Please input all fields.')
    
    if secure_filename(cover.filename).rsplit('.', 1)[-1].lower() not in current_app.config['ALLOWED_EXTENSIONS']:
        return bad_request('Image must be in jpg, jpeg or png')

    book = Book(title=title, description=description, cover=base64.b64encode(cover.stream.read()))
    db.session.add(book)
    db.session.commit()

    return jsonify(book.get_book_info()), 201


@bp.route('/books/<book_id>', methods=['GET'])
@jwt_required()
def book_details(book_id):
    book = Book.query.filter_by(id=book_id).first()

    if not book:
        return not_found('Book\'s not found.')

    return jsonify(book.get_book_info())


@bp.route('/books/<book_id>', methods=['PUT'])
@jwt_required()
def book_update(book_id):
    book = Book.query.filter_by(id=book_id).first()

    if not book:
        return not_found('Book\'s not found.')

    title = request.form['title']
    description = request.form['description']
    cover = request.files['cover']

    if not title or not description or not cover:
        return bad_request('Please input all fields.')
    
    if secure_filename(cover.filename).rsplit('.', 1)[-1].lower() not in current_app.config['ALLOWED_EXTENSIONS']:
        return bad_request('Image must be in jpg, jpeg or png')

    book.title = title
    book.description = description
    book.cover = base64.b64encode(cover.stream.read())

    db.session.commit()

    return jsonify(book.get_book_info())


@bp.route('/books/<book_id>', methods=['DELETE'])
@jwt_required()
def book_deletion(book_id):
    book = Book.query.filter_by(id=book_id).first()

    if not book:
        return not_found('Book\'s not found.')

    db.session.delete(book)
    db.session.commit()

    return jsonify({'message': 'Book deleted successfully.'})


@bp.route('/books/<book_id>/genres', methods=['POST'])
@jwt_required()
def book_add_genre(book_id):
    try:
        book = Book.query.filter_by(id=book_id).first()

        if not book:
            return not_found('Book\'s not found.')

        data = request.get_json()

        Schema({
            'type': And(
                Use(str),
                lambda e: len(e) <= 20,
                error='Genre type must not be more than 20 characters.'
            )
        }).validate(data)

        genre = Genre.query.filter_by(type=data['type']).first()

        if not genre:
            return not_found('Genre\'s not found.')

        book.genres.append(genre)

        db.session.commit()

        return jsonify(book.get_book_genre()), 201
    except SchemaError as e:
        return bad_request(e.errors[-1])


@bp.route('/books/<book_id>/genres', methods=['GET'])
@jwt_required()
def book_genre_list(book_id):
    book = Book.query.filter_by(id=book_id).first()

    if not book:
        return not_found('Book\'s not found.')

    return jsonify(book.get_book_genre())


@bp.route('/books/<book_id>/genres/<genre_id>', methods=['DELETE'])
@jwt_required()
def book_genre_deletion(book_id, genre_id):
    book = Book.query.filter_by(id=book_id).first()

    if not book:
        return not_found('Book\'s not found.')

    book_genre = BookGenre.query.filter_by(book_id=book_id).filter_by(genre_id=genre_id).first()

    if not book_genre:
        return bad_request('Invalid book_id or genre_id.')

    db.session.delete(book_genre)
    db.session.commit()

    return jsonify(book.get_book_genre())

@bp.route('/books/<book_id>/reviews', methods=['POST'])
@jwt_required()
def book_add_review(book_id):
    try:
        data = request.get_json()

        book = Book.query.filter_by(id=book_id).first()

        if not book:
            return not_found('Book\'s not found.')

        Schema({
            'content': Use(str),
            'overview': And(
                Use(str),
                lambda e: len(e) <= 50,
                error='Overview must not be over 50 characters.'
            ),
            'star': And(
                Use(int),
                lambda e: e <= 5 and e >= 0,
                error='Star must be in between 0 to 5 stars.'
            ),
            'started': And(
                Use(str),
                lambda e: validate_date(e),
                error='Invalid starting date.'
            ),
            'finished': And(
                Use(str),
                lambda e: validate_date(e),
                error='Invalid finishing date.'
            )
        }).validate(data)

        review = Review(
            user_id=current_user.id,
            book_id=book_id,
            overview=data['overview'],
            content=data['content'],
            star=data['star'],
            started=data['started'],
            finished=data['finished']
        )

        book.reviews.append(review)
        db.session.commit()

        return jsonify(book.get_book_reviews()), 201
    except SchemaError as e:
        return bad_request(e.errors[-1])


@bp.route('/books/<book_id>/reviews', methods=['GET'])
@jwt_required()
def book_reviews(book_id):
    book = Book.query.filter_by(id=book_id).first()

    if not book:
        return not_found('Book\'s not found.')

    return jsonify(book.get_book_reviews())


@bp.route('/books/<book_id>/reviews/<review_id>', methods=['PUT'])
@jwt_required()
def book_update_review(book_id, review_id):
    try:
        data = request.get_json()

        book = Book.query.filter_by(id=book_id).first()

        if not book:
            return not_found('Book\'s not found.')

        Schema({
            'content': Use(str),
            'overview': And(
                Use(str),
                lambda e: len(e) <= 50,
                error='Overview must not be over 50 characters.'
            ),
            'star': And(
                Use(int),
                lambda e: e <= 5 and e >= 0,
                error='Star must be in between 0 to 5 stars.'
            ),
            'started': And(
                Use(str),
                lambda e: validate_date(e),
                error='Invalid starting date.'
            ),
            'finished': And(
                Use(str),
                lambda e: validate_date(e),
                error='Invalid finishing date.'
            )
        }).validate(data)

        review = Review.query.filter_by(id=review_id).first()

        if not review:
            return not_found('Review\'s not found.')

        review.overview=data['overview'],
        review.content=data['content'],
        review.star=data['star'],
        review.started=data['started'],
        review.finished=data['finished']

        db.session.commit()

        return jsonify(book.get_book_reviews()), 201
    except SchemaError as e:
        return bad_request(e.errors[-1])


@bp.route('/books/<book_id>/reviews/<review_id>', methods=['DELETE'])
@jwt_required()
def book_review_deletion(book_id, review_id):
    book = Book.query.filter_by(id=book_id).first()

    if not book:
        return not_found('Book\'s not found.')

    review = Review.query.filter_by(id=review_id).first()

    if not review:
        return not_found('Review\'s not found.')

    db.session.delete(review)
    db.session.commit()

    return jsonify(book.get_book_reviews())