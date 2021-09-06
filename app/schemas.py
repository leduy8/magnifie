from app import ma
from app.models import User, Book, Category, Comment, Community, Create, Genre, Join, Post, Review, Publish, Strength, Role, Visibility, BookGenre


class UserSchema(ma.SQLAlchemySchema):
    class Meta:
        model = User
    
    id = ma.auto_field()
    email = ma.auto_field()
    name = ma.auto_field()
    member_since = ma.auto_field()
    bio = ma.auto_field()
    born = ma.auto_field()
    website = ma.auto_field()
    social_media = ma.auto_field()
    avatar = ma.auto_field()
    is_author = ma.auto_field()


class RoleSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Role
    
    id = ma.auto_field()
    type = ma.auto_field()


class BookSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Book

    id = ma.auto_field()
    title = ma.auto_field()
    description = ma.auto_field()
    cover = ma.auto_field()
    

class GenreSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Genre


class VisibilitySchema(ma.SQLAlchemySchema):
    class Meta:
        model = Visibility

    id = ma.auto_field()
    type = ma.auto_field()


class CommunitySchema(ma.SQLAlchemySchema):
    class Meta:
        model = Community

    id = ma.auto_field()
    name = ma.auto_field()
    description = ma.auto_field()
    restrict_posting = ma.auto_field()
    visibility = ma.Nested(VisibilitySchema())
    category = ma.Nested(CategorySchema())





