from app import create_app, db
from app.models import User, Book, Category, Comment, Community, Create, Genre, Join, Post, Review, Publish, Strength, Role, Visibility, BookGenre

app = create_app()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

@app.shell_context_processor
def make_shell_context():
    return {
        'db': db,
        'User': User, 
        'Book': Book, 
        'Category': Category, 
        'Comment': Comment, 
        'Community': Community, 
        'Create': Create, 
        'Genre': Genre, 
        'Join': Join, 
        'Post': Post, 
        'Review': Review, 
        'Publish': Publish, 
        'Strength': Strength, 
        'Role': Role, 
        'Visibility': Visibility,
        'BookGenre': BookGenre
    }