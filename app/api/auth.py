from flask import request, jsonify
from schema import SchemaError, Schema, And, Use
from flask_jwt_extended import jwt_required, current_user, create_access_token, create_refresh_token
from app import db, jwt
from app.models import Genre, Strength, User
from app.api import bp
from app.api.errors import not_found, bad_request
from app.utils import validate_mail, is_valid_url
from app.schemas import UserSchema

@jwt.user_identity_loader
def user_identity_lookup(user_id):
    return user_id


@jwt.user_lookup_loader
def user_lookup_callback(_jwt_header, jwt_data):
    identity = jwt_data["sub"]
    return User.query.filter_by(id=identity).first()


@bp.route('/users', methods=['POST'])
def user_register():
    try:
        data = request.get_json()
        Schema({
            'email': And(
                Use(str),
                lambda e: validate_mail(e),
                error='Invalid email'
            ),
            'password': And(
                Use(str),
                lambda p: len(p) >= 6,
                error='Password must be at least 6 characters'
            ),
            'name': And(
                Use(str),
                lambda p: len(p) >= 2,
                error='Name must be at least 2 characters'
            )
        }).validate(data)
        if User.query.filter_by(email=data['email']).first():
            return bad_request('Email is already in used.')
        
        user = User(
            email=data['email'],
            name=data['name'],
        )
        user.set_password(data['password'])

        db.session.add(user)
        db.session.commit()

        return jsonify(UserSchema().dump(user)), 201
    except SchemaError as e :
        return bad_request(e.errors[-1])


@bp.route('/auth', methods=['POST'])
def user_login():
    try:
        data = request.get_json()
        Schema({
            'email': And(
                Use(str),
                lambda e: validate_mail(e),
                error='Invalid email.'
            ),
            'password': And(
                Use(str),
                lambda e: len(e) >= 6,
                error='Password must be at least 6 characters.'
            )
        }).validate(data)

        user = User.query.filter_by(email=data['email']).first()

        if not user:
            return not_found('User\'s not found.')

        if user.check_password(data['email']):
            return bad_request('Wrong password.')

        access_token = create_access_token(identity=user.id)
        refresh_token = create_refresh_token(user.id)

        return jsonify({'access_token': access_token, 'refresh_token': refresh_token})
    except SchemaError as e:
        return bad_request(e.errors[-1])


@bp.route('/users/me', methods=['GET'])
@jwt_required()
def user_profile():
    return jsonify(UserSchema().dump(current_user))
    

@bp.route('users/me', methods=['PUT'])
@jwt_required()
def user_update():
    try:
        data = request.get_json()
        Schema({
            'name': And(
                Use(str),
                lambda e: len(e) >= 2,
                error='Name must be at least 2 characters.'
            ),
            'social_media': And(
                Use(str),
                lambda e: is_valid_url(e),
                error='Social media must be a valid url link.'
            ),
            'bio': And(
                Use(str),
                lambda e: len(e) <= 250,
                error='Bio must not be more than 250 characters.'
            ),
            'born': And(
                Use(str),
                lambda e: len(e) <= 100,
                error='Bio must not be more than 100 characters.'
            ),
            'website': And(
                Use(str),
                lambda e: is_valid_url(e),
                error='Website must be a valid url link.'
            )
        }).validate(data)

        current_user.name = data['name']
        current_user.bio = data['bio']
        current_user.born = data['born']
        current_user.website = data['website']
        current_user.social_media = data['social_media']

        db.session.commit()
        return jsonify(UserSchema().dump(current_user))
    except SchemaError as e:
        return bad_request(e.errors[-1])


@bp.route('/users/<id>', methods=['GET'])
def user_lookup(id):
    user = User.query.filter_by(id=id).first()

    if not user:
        return not_found('User\'s not found.')

    return jsonify(UserSchema().dump(user))


@bp.route('/users/me/genres', methods=['GET'])
@jwt_required()
def user_genres():
    return jsonify(current_user.get_user_genre())


@bp.route('/users/me/genres', methods=['POST'])
@jwt_required()
def user_add_genre():
    try:
        data = request.get_json()
        Schema({
            'type': And(
                Use(str),
                lambda e: len(e) <= 20,
                error='Type must not be more than 20 characters.'
            )
        }).validate(data)

        genre = Genre.query.filter_by(type=data['type']).first()

        if not genre:
            return bad_request('Genre does not exists.')

        if genre in current_user.strength:
            return bad_request(f"User has already added {data['type']}")
        
        current_user.strength.append(genre)
        db.session.commit()

        return jsonify(current_user.get_user_genre()), 201
    except SchemaError as e:
        return e.errors[-1]


@bp.route('/users/me/genres/<genre_id>', methods=['DELETE'])
@jwt_required()
def user_remove_genre(genre_id):
    strength = Strength.query.filter_by(user_id=current_user.id).filter_by(genre_id=genre_id).first()

    if not strength:
        return not_found('User\'s genre not found.')

    db.session.delete(strength)
    db.session.commit()

    return jsonify(current_user.get_user_genre())


@bp.route('/users/me/books', methods=['GET'])
@jwt_required()
def get_user_books():
    return jsonify(current_user.get_user_books())