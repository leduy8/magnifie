from werkzeug.utils import redirect
from flask import url_for
from app.api import bp

@bp.route('/images/<filename>')
def get_image(filename):
    return redirect(url_for('static', filename='images/' + filename), code=301)