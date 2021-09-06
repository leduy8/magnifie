from flask import request, jsonify
from app import db
from app.models import User
from app.api import bp
from app.api.errors import not_found, bad_request

@bp.route('/users', methods=['POST'])
def user_register():
    data = request.get_json()

    if 'name' not in data['name'] or 'email' not in data['email'] or 'password' not in data['password']:
        return bad_request('Please fill in all fields.')

    if User.query.filter_by(email=data['email']).first():
        return bad_request('Email is already in used.')
    
    user = User(
        email=data['email'],
        name=data['name'],
    )
    user.set_password(data['password'])

    db.session.add(user)
    db.session.commit()

    return jsonify(user.get_user_info()), 201


