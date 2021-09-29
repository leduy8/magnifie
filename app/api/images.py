from werkzeug.utils import redirect
from flask import url_for, current_app, send_file
from app.api import bp

@bp.route('/images/<filename>')
def get_image(filename):
    # return redirect(url_for('static', filename='images/' + filename), code=301)
    return send_file(f"{current_app.config['IMAGE_FOLDER_DIR']}/{filename}", as_attachment=True, attachment_filename=filename)