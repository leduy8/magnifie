# Magnifie
## A social media for book's lovers

Magnifie is social media platform where you can find and review any book you want. Also, you can explore clubs that share same interests as you!

## Feature
- Search for books by names or categories.
- Search for other users, clubs by names.
- Featuring best-selling books, most-viewed books, etc. to find out what's trending.
- Allow users to create posts in their wall and comment on others posts.
- Create clubs, manage clubs, posts and comments, etc.

## Tech

Tallie uses a number of framework in the following:
- Flask
- Flask-SQLAlchemy
- Flask-JWT-Extended
- Flask Mail
- Jinja2
- Elasticsearch
- PostgreSQL

## Installation

Tallie requires Python 3.7.9+ to run.

```sh
cd magnifie
```

Accessing virtual environment
- On Windows
```sh
.\venv\Scripts\activate
```

- On MacOS or Linux
```sh
source venv\bin\activate
```

Install require packages and run the server.
```sh
pip install -r requirements.txt
flask run
```