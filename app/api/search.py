from sqlalchemy import or_, and_
from flask import request, jsonify, current_app
from flask_jwt_extended import jwt_required, current_user
from app.api import bp
from app.api.errors import bad_request, not_found
from app.models import User, Book, Community
from app.schemas import UserSchema, BookSchema, CommunitySchema


@bp.route('/search/users', methods=['GET'])
@jwt_required()
def search_users():
    query = request.args.get('query', type=str)

    if not query:
        return bad_request('Search query must have value.')

    users = User.query.filter(or_(User.name.ilike(f'%{query}%'), User.email.ilike(f'%{query}%'))).all()

    return jsonify(UserSchema(many=True).dump(users))


@bp.route('/search/books', methods=['GET'])
@jwt_required()
def search_books():
    query = request.args.get('query', type=str)

    if not query:
        return bad_request('Search query must have value.')

    books = Book.query.filter(Book.title.ilike(f'%{query}%')).all()

    return jsonify(BookSchema(many=True).dump(books))


@bp.route('/search/communities', methods=['GET'])
@jwt_required()
def search_communities():
    query = request.args.get('query', type=str)

    if not query:
        return bad_request('Search query must have value.')

    communities = Community.query.filter(Community.name.ilike(f'%{query}%')).all()

    return jsonify(CommunitySchema(many=True).dump(communities))