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

from backend.mail import send_email

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


@bp.route("/plans", methods=("GET", "POST"))
def plans():
    user = g.user
    if user is None:
        return redirect(url_for("auth.login"))

    if request.method == "POST":
        plan = request.form["plan"]
        try:
            user_id = user.get("id")
            user_email = user.get("email")
            plan = plan.upper()
            body = f"""
            The following user requested a new plan:
            User ID: {user_id}
            User email: {user_email}
            Plan: {plan}
            """
            admin_email = (
                "kandersonko@gmail.com"  # TODO Change this to real administrator email
            )
            send_email(subject="New Plan Request", body=body, recipients=[admin_email])
            return redirect(url_for("index"))
        except Error as e:
            logging.debug(f"Error plan update: {e} ===")

    return render_template("plans/plans.html")


@bp.route("/register", methods=("GET", "POST"))
def register():
    """Register a new user.
    Validates that the email is not already taken. Hashes the
    password for security.
    """
    if request.method == "POST":
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
                return render_template(
                    "auth/register.html", error=[error], isError=True
                )

            # check if user exists
            try:
                stored_user = manager.get_user_by_email(email)
                if stored_user is not None:
                    error = "Invalid email or password"
            except Error as e:
                logging.debug(f"=== Error registration: {e} ===")

            if error is None:
                password_hash = generate_password_hash(password)
                try:
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
                        return redirect(url_for("auth.activation"))
                except Error as e:
                    logging.debug(f"=== Error registration: {e} ===")
            else:
                return render_template(
                    "auth/register.html", error=[error], isError=True
                )

    return render_template("auth/register.html", error=[], isError=False)


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
                return redirect(url_for("auth.activate"))
            return redirect(url_for("index"))

    return render_template("auth/login.html", error=[error], isError=False)


@bp.route("/forgot_password", methods=("GET", "POST"))
def forgot_password():
    if request.method == "POST":
        email = request.form["email"]
        token = generate_token(email)
        reset_link = url_for("auth.reset", token=token)
        body = f"Here is your password reset link: {request.base_url.split('auth/forgot_password')[0][:-1]}{reset_link}"
        send_email(subject="Password Reset Link", body=body, recipients=[email])
        flash(f"Password reset link sent to your email {email}")

    return render_template("auth/forgot_password.html")


@bp.route("/activation", methods=("GET", "POST"))
def activation():
    if request.method == "POST":
        user = g.user
        if user is None:
            return redirect(url_for("auth.login"))

        email = user.get("email")
        token = generate_token(user["email"])
        confirm_url = url_for("auth.activate", token=token)
        body = f"Here is your account activation link: {request.base_url.split('auth/activation')[0][:-1]}{confirm_url}"
        send_email(subject="Account Activation Link", body=body, recipients=[email])
        return redirect(url_for("index"))

    return render_template("auth/activation.html")


@bp.route("/reset/<token>", methods=("GET", "POST"))
def reset(token):
    if request.method == "POST":
        email = request.form["email"]
        old_password = request.form["old_password"]
        new_password = request.form["new_password"]

        user = None
        error = None
        if confirm_token(token) != email:
            flash("Invalid token or email")
        else:
            try:
                user = manager.get_user_by_email(email)

            except Error as e:
                logging.debug(f"=== Error login: {e} ===")
                return render_template("auth/login.html", error=[error], isError=True)
            if user is not None:
                if check_password_hash(user["password"], old_password) == False:
                    error = "Incorrect email or password."
                    return render_template(
                        "auth/forgot_password.html", error=[error], isError=True
                    )
                else:
                    new_password_hash = generate_password_hash(new_password)
                    try:
                        user = manager.reset_password(email, new_password_hash)
                    except Error as e:
                        logging.debug(f"Error password reset {e}")
                    flash("Password reset successfully!")
                    return redirect(url_for("index"))

    return render_template("auth/reset.html")


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
