from flask_jwt_extended.view_decorators import jwt_required
from schema import Schema, SchemaError, And, Use
from flask import request, jsonify, current_app
from flask_jwt_extended import current_user
from app import db
from app.models import Community, Post, Comment, Visibility, Category
from app.schemas import CommunitySchema, PostSchema, CommentSchema
from app.api import bp
from app.api.errors import bad_request, not_found


@bp.route('/communities', methods=['POST'])
@jwt_required()
def community_creation():
    try:
        data = request.get_json()

        Schema({
            'name': And(
                Use(str),
                lambda e: len(e) >= 5 and len(e) <= 100,
                error='Community name must be between 5 and 100 characters.'
            ),
            'description': And(
                Use(str),
                lambda e: len(e) <= 100,
                error='Description must not be more than 100 characters.'
            ),
            'restrict_posting': And(
                Use(bool),
                error='Restrict posting must be a boolean.'
            ),
            'visibility': Use(str),
            'category': Use(str)
        }).validate(data)

        if Community.query.filter_by(name=data['name']).first():
            return bad_request('Community name is already taken.')
        
        visibility = Visibility.query.filter_by(type=data['visibility']).first()

        if not visibility:
            return not_found("Visibility type's not found.")

        category = Category.query.filter_by(type=data['category']).first()

        if not category:
            return not_found("Category type's not found.")

        community = Community(
            name=data['name'],
            description=data['description'],
            restrict_posting=data['restrict_posting'],
            visibility = visibility,
            category = category
        )

        current_user.communities.append(community)
        db.session.add(community)
        db.session.commit()

        return jsonify(CommunitySchema().dump(community)), 201
    except SchemaError as e:
        return bad_request(e.errors[-1])


@bp.route('/communities/<community_id>', methods=['GET'])
@jwt_required()
def community_details(community_id):
    community = Community.query.filter_by(id=community_id).first()

    if not community:
        return not_found("Community's not found.")

    return jsonify(CommunitySchema().dump(community))


@bp.route('/communities/joined', methods=['GET'])
@jwt_required()
def communities_joined():
    return jsonify(current_user.get_user_communities())


@bp.route('/communities/<community_id>/posts', methods=['POST'])
@jwt_required()
def community_create_post(community_id):
    try:
        data = request.get_json()

        community = Community.query.filter_by(id=community_id).first()

        if not community:
            return not_found("Commnunity's not found.")

        Schema({
            'content': And(
                Use(str),
                error='Content must be text.'
            ),
            'turn_off_commenting': And(
                Use(bool),
                error='Commenting option must be a boolean.'
            )
        }).validate(data)

        post = Post(
            content=data['content'],
            turn_off_commenting=data['turn_off_commenting'],
            author_id=current_user.id,
            community_id=community_id
        )

        db.session.add(post)
        community.posts.append(post)
        db.session.commit()

        return jsonify(PostSchema().dump(post)), 201
    except SchemaError as e:
        return jsonify(e.errors[-1])


@bp.route('/communities/<community_id>/posts', methods=['GET'])
@jwt_required()
def community_posts(community_id):
    community = Community.query.filter_by(id=community_id).first()

    if not community:
        return not_found("Commnunity's not found.")

    return jsonify(community.get_community_posts())


@bp.route('/communities/<community_id>/posts/<post_id>', methods=['PUT'])
@jwt_required()
def community_edit_post(community_id, post_id):
    try:
        data = request.get_json()

        community = Community.query.filter_by(id=community_id).first()

        if not community:
            return not_found("Commnunity's not found.")

        Schema({
            'content': And(
                Use(str),
                error='Content must be text.'
            ),
            'turn_off_commenting': And(
                Use(bool),
                error='Commenting option must be a boolean.'
            )
        }).validate(data)

        post = Post.query.filter_by(id=post_id).first()

        if not post:
            return not_found("Post's not found.")

        post.content = data['content']
        post.turn_off_commenting = data['turn_off_commenting']

        db.session.commit()

        return jsonify(PostSchema().dump(post))
    except SchemaError as e:
        return jsonify(e.errors[-1])


@bp.route('/communities/<community_id>/posts/<post_id>', methods=['DELETE'])
@jwt_required()
def community_delete_post(community_id, post_id):
    community = Community.query.filter_by(id=community_id).first()

    if not community:
        return not_found("Commnunity's not found.")

    post = Post.query.filter_by(id=post_id).first()

    if not post:
        return not_found("Post's not found.")

    community.posts.remove(post)
    db.session.delete(post)
    db.session.commit()

    return jsonify(community.get_community_posts())


@bp.route('/communities/<community_id>/posts/<post_id>/comments', methods=['POST'])
@jwt_required()
def community_comment_creation(community_id, post_id):
    try:
        data = request.get_json()

        community = Community.query.filter_by(id=community_id).first()

        if not community:
            return not_found("Commnunity's not found.")

        post = Post.query.filter_by(id=post_id).first()

        if not post:
            return not_found("Post's not found.")

        Schema({
            'content': And(
                Use(str),
                error='Comment content must be text.'
            )
        }).validate(data)

        comment = Comment(
            user_id=current_user.id,
            post_id=post_id,
            content=data['content']
        )

        post.comments.append(comment)
        db.session.add(comment)
        db.session.commit()

        return jsonify(CommentSchema().dump(comment)), 201
    except SchemaError as e:
        return bad_request(e.errors[-1])


@bp.route('/communities/<community_id>/posts/<post_id>/comments', methods=['GET'])
@jwt_required()
def community_post_comments(community_id, post_id):
    community = Community.query.filter_by(id=community_id).first()

    if not community:
        return not_found("Commnunity's not found.")

    post = Post.query.filter_by(id=post_id).first()

    if not post:
        return not_found("Post's not found.")

    return jsonify(post.get_post_comments())


@bp.route('/communities/<community_id>/posts/<post_id>/comments/<comment_id>', methods=['PUT'])
@jwt_required()
def community_edit_post_comment(community_id, post_id, comment_id):
    try:
        data = request.get_json()

        community = Community.query.filter_by(id=community_id).first()

        if not community:
            return not_found("Commnunity's not found.")

        post = Post.query.filter_by(id=post_id).first()

        if not post:
            return not_found("Post's not found.")

        Schema({
            'content': And(
                Use(str),
                error='Comment content must be text.'
            )
        }).validate(data)

        comment = Comment.query.filter_by(id=comment_id).first()

        if not comment:
            return not_found("Comment's not found.")

        comment.content = data['content']

        db.session.commit()

        return jsonify(CommentSchema().dump(comment))
    except SchemaError as e:
        return bad_request(e.errors[-1])


@bp.route('/communities/<community_id>/posts/<post_id>/comments/<comment_id>', methods=['DELETE'])
@jwt_required()
def community_delete_post_comment(community_id, post_id, comment_id):
    community = Community.query.filter_by(id=community_id).first()

    if not community:
        return not_found("Commnunity's not found.")

    post = Post.query.filter_by(id=post_id).first()

    if not post:
        return not_found("Post's not found.")

    comment = Comment.query.filter_by(id=comment_id).first()

    if not comment:
        return not_found("Comment's not found.")

    post.comments.remove(comment)
    db.session.delete(comment)
    db.session.commit()

    return jsonify(post.get_post_comments())