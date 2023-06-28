from flask import Blueprint, render_template
from backend.utils import add_security_headers

bp = Blueprint("modules", __name__)


@bp.route("/modules")
def index():
    return add_security_headers(render_template("modules/modules.html"))


@bp.route("/modules/ci_user")
def ci_user():
    return add_security_headers(render_template("modules/ci_user.html"))


@bp.route("/modules/ci_educator")
def ci_educator():
    return add_security_headers(render_template("modules/ci_educator.html"))


@bp.route("/modules/ci_crowdsourcing")
def ci_crowdsourcing():
    return add_security_headers(render_template("modules/ci_crowdsourcing.html"))


@bp.route("/modules/ci_competition")
def ci_competition():
    return add_security_headers(render_template("modules/ci_competition.html"))
