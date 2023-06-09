from flask import Blueprint, render_template
from backend.utils import add_security_headers

bp = Blueprint("home", __name__)


@bp.route("/")
def index():
    return add_security_headers(render_template("index.html"))
