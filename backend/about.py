from flask import Blueprint, render_template
from backend.utils import add_security_headers

bp = Blueprint("about", __name__)


@bp.route("/about")
def index():
    return add_security_headers(render_template("about.html"))
