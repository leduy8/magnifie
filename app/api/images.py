from flask import current_app, send_file
from app.api import bp

@bp.route('/images/<filename>')
def get_image(filename):
    # return send_file(f"{current_app.config['IMAGE_FOLDER_DIR']}\\{filename}", as_attachment=True, attachment_filename=filename)
    return send_file(f"{current_app.config['IMAGE_FOLDER_DIR']}/{filename}", as_attachment=True, attachment_filename=filename)