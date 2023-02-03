from flask import Blueprint
from flask import request, render_template, g, redirect, url_for, flash 
from flask import session
from werkzeug.security import check_password_hash, generate_password_hash

from lca_tool.db import get_db


bp = Blueprint("auth", __name__, url_prefix="/auth")


@bp.before_app_request
def load_logged_in_user():
    """If a user id is stored in the session, load the user object from
    the database into ``g.user``."""
    user_id = session.get("user_id")

    if user_id is None:
        g.user = None
    else:
        g.user = (
            get_db().execute("SELECT * FROM user WHERE id = ?", (user_id,)).fetchone()
            )
            
@bp.route("/register", methods=("GET", "POST"))
def register():
    """Register a new user.
    Validates that the username is not already taken. Hashes the
    password for security.
    """
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        email = request.form["email"]
        confirm_password = request.form["confirm_password"]
        first_name = request.form["first_name"]
        last_name = request.form["last_name"]
        affiliation = request.form["affiliation"]
        db = get_db()
        error = None

        if not username:
            error = "Username is required."
        elif not password:
            error = "Password is required."
        elif not confirm_password:
            error = "Password confirmation is required."
        elif confirm_password != password:
            error = "The two passwords do not match."
        elif not email:
            error = "The email is required."
        elif not first_name:
            error = "The fist name is required."
        elif not last_name:
            error = "The Last name is required."
        elif not affiliation:
            error = "The Affiliation is required."

        if error is None:
            try:
                db.execute(
                    "INSERT INTO user (username, password, email, first_name, last_name, affiliation) VALUES (?, ?, ?, ?, ?, ?)",
                    (username, generate_password_hash(password), email, first_name, last_name, affiliation),
                )
                db.commit()
            except db.IntegrityError:
                # The username was already taken, which caused the
                # commit to fail. Show a validation error.
                error = f"User {username} and/or email {email} is already registered."
            else:
                # Success, go to the login page.
                return redirect(url_for("auth.login"))

        flash(error)

    return render_template("auth/register.html")



@bp.route("/login", methods=("GET", "POST"))
def login():
    """Log in a registered user by adding the user id to the session."""
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        db = get_db()
        error = None
        user = db.execute(
            "SELECT * FROM user WHERE username = ?", (username,)
        ).fetchone()

        if user is None:
            error = "Incorrect username."
        elif not check_password_hash(user["password"], password):
            error = "Incorrect password."

        if error is None:
            # store the user id in a new session and return to the index
            session.clear()
            session["user_id"] = user["id"]
            return redirect(url_for("index"))

        flash(error)

    return render_template("auth/login.html")


@bp.route("/logout")
def logout():
    """Clear the current session, including the stored user id."""
    session.clear()
    return redirect(url_for("index"))
