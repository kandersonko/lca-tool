from flask import Blueprint, render_template
from werkzeug.utils import secure_filename
from flask import current_app, flash
from flask import request, g, redirect, url_for
from flask import session
import logging
from pathlib import Path
import os

from mysql.connector import Error

from backend.utils import add_security_headers, allowed_file

from backend.db import DBManager

bp = Blueprint("datasets", __name__)


@bp.route("/datasets")
def index():
    return add_security_headers(render_template("datasets/index.html"))


@bp.route('/datasets/upload', methods=['POST'])
def upload_file():
    user_id = session.get("user_id")
    logging.debug("=== Uploading files: %s", user_id)

    if user_id is None:
        g.user = None
        flash("You need to login to upload your datasets!")
        return redirect(url_for("auth.login"))
    else:
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            try:
                manager = DBManager.instance(
                    password_file=current_app.config["DB_PASSWORD"]
                )
                plan = manager.get_plan_by_user_id(user_id)
            except Error as e:
                logging.debug(f"=== Failed to get user plan: {e} ===")

                if plan is None:
                    flash("You have not subscribed to a plan!")
                    return redirect(url_for("auth.plans"))
                else:
                    # if plan.get('tier') == 'free':
                    # TODO check file size
                    filename = secure_filename(file.filename)
                    user_storage = plan.get("storage_url")
                    upload_path = Path('data/') / user_storage
                    file.save(os.path.join(upload_path, filename))
                    flash("File uploaded successfully")
                    return redirect(url_for("datasets.index"), file=file)
