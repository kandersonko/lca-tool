import os
from flask import Blueprint
from flask import request, render_template, g, redirect, url_for, flash
from flask import session
from werkzeug.security import check_password_hash, generate_password_hash

# import logging

from backend.db import manager
from mysql.connector import Error

bp = Blueprint("auth", __name__, url_prefix="/auth")


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
            print(f"=== User: {g.user} ")
        except Error as e:
            print(f"=== load_logged_in_user error: {e} ===")


@bp.route("/register", methods=("GET", "POST"))
def register():
    """Register a new user.
    Validates that the email is not already taken. Hashes the
    password for security.
    """
    print(f"request: {request}")
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        confirm_password = request.form["confirm_password"]
        first_name = request.form["first_name"]
        last_name = request.form["last_name"]
        affiliation = request.form["affiliation"]
        print(f"Register: {email} | {password}")
        error = None
        if confirm_password != password:
            error = "The password should matched."

        if error is None:
            password_hash = generate_password_hash(password)
            try:
                manager.create_user(
                    first_name=first_name,
                    last_name=last_name,
                    email=email,
                    password_hash=password_hash,
                    affiliation=affiliation,
                )
                g.user = manager.get_user_by_email(email)
                if g.user:
                    session["user_id"] = g.user["id"]
                return redirect(url_for("index"))

            except Error as e:
                # The email was already taken, which caused the
                # commit to fail. Show a validation error.
                print(f"Failed to register user: {e} ===")
                error = f"User with email {email} is already registered."
        else:
            flash(error)

    return render_template("auth/register.html")


@bp.route("/login", methods=("GET", "POST"))
def login():
    """Log in a registered user by adding the user id to the session."""
    print("Login request: ", request)
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        error = None
        user = None
        print(f"=== Login: {email} | {password} | {user}")
        try:
            user = manager.get_user_by_email(email)
            if user is None:
                error = "The user does not have an account."
            print(f"Login user found: {user}")

        except Error as e:
            print(f"=== Error login: {e} ===")

        if check_password_hash(user["password"], password) == False:
            error = "Incorrect email or password."
        else:
            session.clear()
            session["user_id"] = user["id"]
            return redirect(url_for("index"))

    return render_template("auth/login.html")


@bp.route("/logout")
def logout():
    """Clear the current session, including the stored user id."""
    session.clear()
    return redirect(url_for("index"))
