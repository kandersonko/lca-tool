from flask import Blueprint, render_template
from backend.utils import add_security_headers

bp = Blueprint("gallery", __name__)


@bp.route("/gallery")
def index():
    return add_security_headers(render_template("gallery.html"))