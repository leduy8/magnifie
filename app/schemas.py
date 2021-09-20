from app import ma
from app.models import User, Book, Category, Comment, Community, Genre, Membership, Post, Review, Publish, Strength, Role, Visibility, BookGenre


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
    # strength = ma.auto_field()


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


class CategorySchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Category


class CommunitySchema(ma.SQLAlchemySchema):
    class Meta:
        model = Community

    id = ma.auto_field()
    name = ma.auto_field()
    description = ma.auto_field()
    restrict_posting = ma.auto_field()
    visibility = ma.Nested(VisibilitySchema())
    category = ma.Nested(CategorySchema())


class PostSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Post

    id = ma.auto_field()
    content = ma.auto_field()
    turn_off_commenting = ma.auto_field()
    author = ma.Nested(UserSchema())


class BookGenre(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = BookGenre


class CommentSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Comment

    id = ma.auto_field()
    author = ma.Nested(UserSchema())
    post = ma.Nested(PostSchema())
    content = ma.auto_field()


class ReviewSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Review


class MembershipSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Membership

    id = ma.auto_field()
    profile = ma.Nested(UserSchema())
    role = ma.Nested(RoleSchema())
    community = ma.Nested(CommunitySchema())


class PublishSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Publish
        

class StrengthSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Strength
