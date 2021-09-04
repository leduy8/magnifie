from datetime import date
from werkzeug.security import check_password_hash, generate_password_hash
from sqlalchemy_utils import URLType
from app import db


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(50), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    name = db.Column(db.String(40))
    member_since = db.Column(db.Date, default=date.today)
    bio = db.Column(db.String(250))
    born = db.Column(db.String())
    website = db.Column(URLType)
    social_media = db.Column(URLType)
    is_author = db.Column(db.Boolean, default=False)
    reviews = db.relationship(
        'Book',
        secondary='review',
        backref='reviewed_by',
        lazy='dynamic'
    )
    publishes = db.relationship(
        'Book',
        secondary='publish',
        backref='published_by',
        lazy='dynamic'
    )
    strength = db.relationship(
        'Genre',
        secondary='strength',
        backref='users',
        lazy='dynamic'
    )
    communities = db.relationship(
        'Community',
        secondary='join',
        backref='users',
        lazy='dynamic'
    )
    posts = db.relationship(
        'Post',
        secondary='create',
        backref='posted_by',
        lazy='dynamic'
    )
    comments = db.relationship(
        'Post',
        secondary='comment',
        backref='comments',
        lazy='dynamic'
    )

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self) -> str:
        return f'<User: {self.email}>'

    def __str__(self) -> str:
        return f'{self.email}'


class Role(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(20))

    def __repr__(self) -> str:
        return f'<Role: {self.type}>'

    def __str__(self) -> str:
        return f'{self.type}'


class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50))
    description = db.Column(db.String(250))
    cover = db.Column(db.LargeBinary)

    def __repr__(self) -> str:
        return f'<Book: {self.title}>'

    def __str__(self) -> str:
        return f'{self.title}'


class Genre(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(20))

    def __repr__(self) -> str:
        return f'<Genre: {self.type}>'

    def __str__(self) -> str:
        return f'{self.type}'


class Community(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    description = db.Column(db.String(100))
    restrict_posting = db.Column(db.Boolean, default=False)
    posts = db.relationship('Post', backref='community', lazy='dynamic')
    visibility = db.relationship('Visibility', uselist=False)
    category = db.relationship('Category', uselist=False)

    def __repr__(self) -> str:
        return f'<Community: {self.name}>'

    def __str__(self) -> str:
        return f'{self.name}'


class Visibility(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(20))
    community_id = db.Column(db.Integer, db.ForeignKey('community.id'))

    def __repr__(self) -> str:
        return f'<Visibility: {self.type}>'

    def __str__(self) -> str:
        return f'{self.type}'


class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(20))
    community_id = db.Column(db.Integer, db.ForeignKey('community.id'))

    def __repr__(self) -> str:
        return f'<Category: {self.type}>'

    def __str__(self) -> str:
        return f'{self.type}'


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text)
    turn_off_commenting = db.Column(db.Boolean, default=False)
    community_id = db.Column(db.Integer, db.ForeignKey('community.id'))

    def __repr__(self) -> str:
        return f'<Post: {self.id}>'

    def __str__(self) -> str:
        return f'{self.id}'


class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    book_id = db.Column(db.Integer, db.ForeignKey('book.id'))
    content = db.Column(db.Text)

    def __repr__(self) -> str:
        return f'<Review: {self.id}>'

    def __str__(self) -> str:
        return f'{self.id}'


class Publish(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    book_id = db.Column(db.Integer, db.ForeignKey('book.id'))

    def __repr__(self) -> str:
        return f'<Review: {self.id}>'

    def __str__(self) -> str:
        return f'{self.id}'


class Strength(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    genre_id = db.Column(db.Integer, db.ForeignKey('genre.id'))

    def __repr__(self) -> str:
        return f'<Review: {self.id}>'

    def __str__(self) -> str:
        return f'{self.id}'


class Join(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    community_id = db.Column(db.Integer, db.ForeignKey('community.id'))
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'))


class Create(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'))


class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'))