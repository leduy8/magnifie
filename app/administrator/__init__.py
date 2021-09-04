from werkzeug.exceptions import HTTPException
from flask import Response, redirect
from flask_basicauth import BasicAuth
from flask_admin import Admin
from flask_admin.contrib import sqla
from app import db
from app.models import User, Book, Category, Comment, Community, Create, Genre, Join, Post, Review, Publish, Strength, Role, Visibility

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
        column_exclude_list = ('password_hash')
        form_excluded_columns = ('password_hash', 'member_since')

        def on_model_change(self, form, model, is_created):
            return super().on_model_change(form, model, is_created)

    class BookModelView(ModelView):

        def on_model_change(self, form, model, is_created):
            return super().on_model_change(form, model, is_created)

    class CategoryModelView(ModelView):

        def on_model_change(self, form, model, is_created):
            return super().on_model_change(form, model, is_created)


    class CommentModelView(ModelView):

        def on_model_change(self, form, model, is_created):
            return super().on_model_change(form, model, is_created)

    class CommunityModelView(ModelView):

        def on_model_change(self, form, model, is_created):
            return super().on_model_change(form, model, is_created)
    
    class CreateModelView(ModelView):

        def on_model_change(self, form, model, is_created):
            return super().on_model_change(form, model, is_created)
    
    class GenreModelView(ModelView):

        def on_model_change(self, form, model, is_created):
            return super().on_model_change(form, model, is_created)
    
    class JoinModelView(ModelView):

        def on_model_change(self, form, model, is_created):
            return super().on_model_change(form, model, is_created)
    
    class PostModelView(ModelView):

        def on_model_change(self, form, model, is_created):
            return super().on_model_change(form, model, is_created)
    
    class ReviewModelView(ModelView):

        def on_model_change(self, form, model, is_created):
            return super().on_model_change(form, model, is_created)
    
    class PublishModelView(ModelView):

        def on_model_change(self, form, model, is_created):
            return super().on_model_change(form, model, is_created)
    
    class StrengthModelView(ModelView):

        def on_model_change(self, form, model, is_created):
            return super().on_model_change(form, model, is_created)
    
    class RoleModelView(ModelView):

        def on_model_change(self, form, model, is_created):
            return super().on_model_change(form, model, is_created)
    
    class VisibilityModelView(ModelView):

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
    admin.add_view(JoinModelView(Join, db.session))
    admin.add_view(RoleModelView(Role, db.session))
    admin.add_view(CreateModelView(Create, db.session))
    admin.add_view(PublishModelView(Publish, db.session))
    admin.add_view(StrengthModelView(Strength, db.session))
    admin.add_view(VisibilityModelView(Visibility, db.session))