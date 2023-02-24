import os
from flask import Blueprint, flash
from flask import request, render_template, g, redirect, url_for
from flask import session
from werkzeug.security import check_password_hash, generate_password_hash

from itsdangerous import URLSafeTimedSerializer
import logging

from backend.db import manager
from backend.config import config
from mysql.connector import Error

bp = Blueprint("auth", __name__, url_prefix="/auth")


def generate_token(email):
    serializer = URLSafeTimedSerializer(config["SECRET_KEY"])
    return serializer.dumps(email, salt=config["SECURITY_PASSWORD_SALT"])


def confirm_token(token, expiration=3600):
    serializer = URLSafeTimedSerializer(config["SECRET_KEY"])
    try:
        email = serializer.loads(
            token, salt=config["SECURITY_PASSWORD_SALT"], max_age=expiration
        )
        return email
    except Exception:
        return False


@bp.before_app_request
def load_logged_in_user():
    """If a user id is stored in the session, load the user object from
    the database into ``g.user``."""
    user_id = session.get("user_id")

    if user_id is None:
        g.user = None
    else:
        try:
            g.user = manager.get_user_by_id(user_id)
            logging.debug(f"=== User: {g.user} ")
        except Error as e:
            logging.debug(f"=== load_logged_in_user error: {e} ===")


@bp.route("/register", methods=("GET", "POST"))
def register():
    """Register a new user.
    Validates that the email is not already taken. Hashes the
    password for security.
    """
    error = None
    logging.debug(f"=== Register request: {request}")
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        confirm_password = request.form["confirm_password"]
        first_name = request.form["first_name"]
        last_name = request.form["last_name"]
        affiliation = request.form["affiliation"]
        logging.debug(f"Register: {email} | {password}")
        if confirm_password != password:
            error = "The password should matched."
            return render_template("auth/register.html", error=[error], isError=True)

        if error is None:
            password_hash = generate_password_hash(password)
            g.user = manager.create_user(
                first_name=first_name,
                last_name=last_name,
                email=email,
                password_hash=password_hash,
                affiliation=affiliation,
            )
            if g.user is not None and g.user.get("id"):
                session["user_id"] = g.user["id"]
                logging.debug("=== Create plan after registration")
                manager.create_user_plan(g.user["id"], tier="free")
                token = generate_token(g.user["email"])
                confirm_url = url_for("auth.activate", token=token)
                return render_template("auth/activate.html", confirm_url=confirm_url)
        else:
            return render_template("auth/register.html", error=[error], isError=True)

    return render_template("auth/register.html", error=[error], isError=False)


@bp.route("/login", methods=("GET", "POST"))
def login():
    """Log in a registered user by adding the user id to the session."""
    error = None
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        user = None
        try:
            user = manager.get_user_by_email(email)
            logging.debug(f"=== Login: ", email, password, user)

        except Error as e:
            logging.debug(f"=== Error login: {e} ===")
            return render_template("auth/login.html", error=[error], isError=True)

        if user is None:
            error = "The user does not have an account."
            logging.debug(f"Login user found: {user}")
            return render_template("auth/login.html", error=[error], isError=True)
        elif check_password_hash(user["password"], password) == False:
            error = "Incorrect email or password."
            return render_template("auth/login.html", error=[error], isError=True)
        else:
            session.clear()
            session["user_id"] = user["id"]
            g.user = user
            if user.get("status") != "active":
                token = generate_token(user["email"])
                confirm_url = url_for("auth.activate", token=token)
                return render_template("auth/activate.html", confirm_url=confirm_url)
            else:
                return redirect(url_for("index"))

    return render_template("auth/login.html", error=[error], isError=False)


@bp.route("/activate/<token>")
def activate(token):
    if g.user is None:
        return redirect(url_for("auth.login"))
    else:
        user_email = g.user.get("email")
        status = g.user.get("status")
        email_from_token = confirm_token(token)
        if status == "active":
            flash("Account already active")
            return redirect(url_for("index"))
        elif user_email == email_from_token:
            try:
                manager.activate_user(user_email)
                return redirect(url_for("index"))
            except Error as e:
                logging.debug(f"=== Error account activation: {e}")
                flash("Error during account activation try again")

        else:
            flash("Invalid or expired activation token")

    return render_template("auth/activate.html")


@bp.route("/logout")
def logout():
    """Clear the current session, including the stored user id."""
    session.clear()
    return redirect(url_for("index"))
