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
    avatar = db.Column(db.LargeBinary)
    is_author = db.Column(db.Boolean, default=False)
    reviews = db.relationship(
        'Book',
        secondary='review',
        backref='reviews',
        lazy='dynamic'
    )
    publishes = db.relationship(
        'Book',
        secondary='publish',
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
        lazy='dynamic'
    )

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def get_user_info(self):
        return {
            'id': self.id,
            'email': self.email,
            'name': self.name,
            'member_since': self.member_since,
            'bio': self.bio,
            'born': self.born,
            'website': self.website,
            'social_media': self.social_media,
            'avatar': self.avatar,
            'is_author': self.is_author,
        }

    def get_user_genre(self):
        return {'strengths': [s.get_genre_info() for s in self.strength]}

    def get_user_book(self):
        return {'books': [p.get_book_info() for p in self.publishes]}

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
    genres = db.relationship(
        'Genre',
        secondary='bookgenre',
        backref='books',
        lazy='dynamic'
    )

    def get_book_info(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'cover': self.cover
        }
    
    def get_book_reviews(self):
        return {'reviews': [r.get_review_info() for r in self.reviews]}

    def get_book_genre(self):
        return {'books_genres': [g.get_genre_info() for g in self.genres]}

    def __repr__(self) -> str:
        return f'<Book: {self.title}>'

    def __str__(self) -> str:
        return f'{self.title}'


class Genre(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(20))

    def get_genre_info(self):
        return {
            'id': self.id,
            'type': self.type
        }

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

    def get_community_info(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'restrict_posting': self.restrict_posting,
            'visibility': self.visibility.get_visibility_info(),
            'category': self.category.get_category_info()
        }

    def __repr__(self) -> str:
        return f'<Community: {self.name}>'

    def __str__(self) -> str:
        return f'{self.name}'


class Visibility(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(20))
    community_id = db.Column(db.Integer, db.ForeignKey('community.id'))

    def get_visibility_info(self):
        return {
            'id': self.id,
            'type': self.type
        }

    def __repr__(self) -> str:
        return f'<Visibility: {self.type}>'

    def __str__(self) -> str:
        return f'{self.type}'


class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(20))
    community_id = db.Column(db.Integer, db.ForeignKey('community.id'))

    def get_category_info(self):
        return {
            'id': self.id,
            'type': self.type
        }

    def __repr__(self) -> str:
        return f'<Category: {self.type}>'

    def __str__(self) -> str:
        return f'{self.type}'


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text)
    turn_off_commenting = db.Column(db.Boolean, default=False)
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    community_id = db.Column(db.Integer, db.ForeignKey('community.id'))
    comments = db.relationship(
        'User',
        secondary='comment',
        lazy='dynamic'
    )

    def get_post_info(self):
        return {
            'id': self.id,
            'content': self.content,
            'turn_off_commenting': self.turn_off_commenting,
            'author_id': self.author_id,
            'community_id': self.community_id
        }

    def get_post_comment(self):
        return {'comments': [c.get_comment_info() for c in self.comments]}

    def __repr__(self) -> str:
        return f'<Post: {self.id}>'

    def __str__(self) -> str:
        return f'{self.id}'


class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    book_id = db.Column(db.Integer, db.ForeignKey('book.id'))
    overview = db.Column(db.String(50))
    content = db.Column(db.Text)
    star = db.Column(db.Integer)
    started = db.Column(db.Date)
    finished = db.Column(db.Date)

    def get_review_info(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'book_id': self.book_id,
            'overview': self.overview,
            'content': self.content,
            'star': self.star,
            'started': self.started,
            'finished': self.finished
        }

    def __repr__(self) -> str:
        return f'<Review: {self.id}>'

    def __str__(self) -> str:
        return f'{self.id}'


class BookGenre(db.Model):
    __tablename__ = 'bookgenre'
    id = db.Column(db.Integer, primary_key=True)
    book_id = db.Column(db.Integer, db.ForeignKey('book.id'))
    genre_id = db.Column(db.Integer, db.ForeignKey('genre.id'))
    

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
    content = db.Column(db.Text)

    def get_comment_info(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'post_id': self.post_id,
            'content': self.content
        }