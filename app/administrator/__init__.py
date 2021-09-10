from werkzeug.exceptions import HTTPException
from flask import Response, redirect
from flask_basicauth import BasicAuth
from flask_admin import Admin
from flask_admin.contrib import sqla
from app import db
from app.models import User, Book, Category, Comment, Community, Genre, Membership, Post, Review, Publish, Strength, Role, Visibility, BookGenre

def init_admin(app):
    basic_auth = BasicAuth(app)

    class AuthException(HTTPException):
        def __init__(self, message):
            super().__init__(message, Response(
                message, 
                401,
                {'WWW-Authenticate': 'Basic realm="Login Required"'}
            ))

    class ModelView(sqla.ModelView):
        def is_accessible(self):
            if not basic_auth.authenticate():
                raise AuthException('Not authenticated. Refresh the page.')
            else:
                return True

        def inaccessible_callback(self, name, **kwargs):
            return redirect(basic_auth.challenge())

    class UserModelView(ModelView):
        column_list = ('id', 'email', 'name', 'member_since', 'born', 'website', 'social_media', 'avatar', 'is_author')
        # column_exclude_list = ('password_hash', 'bio')
        form_excluded_columns = ('password_hash', 'member_since', 'reviews', 'posts', 'comments', 'publishes')

        def on_model_change(self, form, model, is_created):
            return super().on_model_change(form, model, is_created)

    class BookModelView(ModelView):
        column_list = ('id', 'title', 'description', 'cover')
        # column_exclude_list = ('cover')
        form_excluded_columns = ('reviewed_by')

        def on_model_change(self, form, model, is_created):
            return super().on_model_change(form, model, is_created)

    class CategoryModelView(ModelView):
        column_list = ('id', 'type', 'community_id')
        form_columns = ('type', 'community_id')

        def on_model_change(self, form, model, is_created):
            return super().on_model_change(form, model, is_created)


    class CommentModelView(ModelView):
        column_list = ('id', 'user_id', 'post_id', 'content')
        form_columns = ('user_id', 'post_id', 'content')

        def on_model_change(self, form, model, is_created):
            return super().on_model_change(form, model, is_created)

    class CommunityModelView(ModelView):
        column_list = ('id', 'name', 'description', 'restrict_posting')
        form_excluded_columns = ('posts', 'users')

        def on_model_change(self, form, model, is_created):
            return super().on_model_change(form, model, is_created)
    
    class GenreModelView(ModelView):
        column_list = ('id', 'type')

        def on_model_change(self, form, model, is_created):
            return super().on_model_change(form, model, is_created)
    
    class MembershipModelView(ModelView):
        column_list = ('id', 'user_id', 'community_id', 'role_id')
        form_columns = ('user_id', 'community_id', 'role_id')

        def on_model_change(self, form, model, is_created):
            return super().on_model_change(form, model, is_created)
    
    class PostModelView(ModelView):
        form_excluded_columns = ('comments')

        def on_model_change(self, form, model, is_created):
            return super().on_model_change(form, model, is_created)
    
    class ReviewModelView(ModelView):
        column_list = ('id', 'user_id', 'book_id', 'content')
        form_columns = ('user_id', 'book_id', 'content')

        def on_model_change(self, form, model, is_created):
            return super().on_model_change(form, model, is_created)
    
    class PublishModelView(ModelView):
        column_list = ('id', 'user_id', 'book_id')
        form_columns = ('user_id', 'book_id')

        def on_model_change(self, form, model, is_created):
            return super().on_model_change(form, model, is_created)
    
    class StrengthModelView(ModelView):
        column_list = ('id', 'user_id', 'genre_id')
        form_columns = ('user_id', 'genre_id')

        def on_model_change(self, form, model, is_created):
            return super().on_model_change(form, model, is_created)
    
    class RoleModelView(ModelView):
        column_list = ('id', 'type')

        def on_model_change(self, form, model, is_created):
            return super().on_model_change(form, model, is_created)
    
    class VisibilityModelView(ModelView):
        column_list = ('id', 'type')

        def on_model_change(self, form, model, is_created):
            return super().on_model_change(form, model, is_created)
    
    class BookGenreModelView(ModelView):
        column_list = ('id', 'book_id', 'genre_id')

        def on_model_change(self, form, model, is_created):
            return super().on_model_change(form, model, is_created)

    admin = Admin(app)
    admin.add_view(UserModelView(User, db.session))
    admin.add_view(BookModelView(Book, db.session))
    admin.add_view(ReviewModelView(Review, db.session))
    admin.add_view(GenreModelView(Genre, db.session))
    admin.add_view(CommunityModelView(Community, db.session))
    admin.add_view(CategoryModelView(Category, db.session))
    admin.add_view(PostModelView(Post, db.session))
    admin.add_view(CommentModelView(Comment, db.session))
    admin.add_view(RoleModelView(Role, db.session))
    admin.add_view(MembershipModelView(Membership, db.session))
    admin.add_view(PublishModelView(Publish, db.session))
    admin.add_view(StrengthModelView(Strength, db.session))
    admin.add_view(VisibilityModelView(Visibility, db.session))
    admin.add_view(BookGenreModelView(BookGenre, db.session))