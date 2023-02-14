import os
import logging
from flask import Flask
from mysql.connector import connect, Error

mysql_connection = None


def db_connection(host="db", database="lca", user="root", password_file=None):
    global mysql_connection
    try:
        mysql_connection = connect(
            user=user,
            password=password_file,
            host=host,  # name of the mysql service as set in the docker compose file
            database=database,
            raise_on_warnings=True,
            auth_plugin="mysql_native_password",
        )
    except Error as e:
        print(f"==== Connection error: {e} ====")


class DBManager:
    def __init__(
        self,
        host="db",
        database="lca",
        user="root",
        password_file="/run/secrets/db-password",
    ):
        pf = open(password_file, "r")
        password = pf.read().strip()
        pf.close()
        print(f"User: {user} | Password: {password}")
        self.connection = None
        self.cursor = None
        self.initialized = False

        try:
            self.connection = connect(
                user=user,
                password=password,
                host=host,  # name of the mysql service as set in the docker compose file
                database=database,
                raise_on_warnings=True,
                auth_plugin="mysql_native_password",
            )
        except Error as e:
            print(f"==== Connection error: {e} ====")

    def _unpack_user(self, query_result):
        if query_result is None:
            return None
        (user_id, first_name, last_name, email, password, affiliation) = query_result
        user = {
            "id": user_id,
            "first_name": first_name,
            "last_name": last_name,
            "email": email,
            "password": password,
            "affiliation": affiliation,
        }
        return user

    def create_users_table(self):
        if self.initialized:
            return
        with self.connection.cursor() as cursor:
            # cursor.execute("DROP TABLE IF EXISTS users")
            # cursor.execute("REPAIR TABLE users")
            try:
                cursor.execute(
                    """
                    CREATE TABLE IF NOT EXISTS users (
                        id INT AUTO_INCREMENT PRIMARY KEY, 
                        first_name VARCHAR(50) NOT NULL,
                        last_name VARCHAR(50) NOT NULL,
                        email VARCHAR(100) NOT NULL UNIQUE,
                        password VARCHAR(255) NOT NULL,
                        affiliation VARCHAR(255) NOT NULL
                    )"""
                )
                self.connection.commit()
                self.initialized = True
                print("=== Database Initialized in db.py ===")

            except Error as e:
                print(f"Error creating table: {e} ===")

    def create_user(self, first_name, last_name, email, password_hash, affiliation):
        with self.connection.cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO users (
                    first_name, 
                    last_name, 
                    email, 
                    password, 
                    affiliation
                ) VALUES (%s, %s, %s, %s, %s)
                """,
                (first_name, last_name, email, password_hash, affiliation),
            )
            self.connection.commit()

    def get_user_by_email(self, email):
        user = {email: ""}
        print(f"=== Retrieving user by email: {email} ===")
        with self.connection.cursor() as cursor:
            cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
            result = cursor.fetchone()
            user = self._unpack_user(result)
            print(f"get_user_by_id result: {result}")
            print(f"=== FOUND user: {user} ===")
        return user

    def get_user_by_id(self, user_id):
        user = None
        print(f"=== Retrieving user by user_id: {user_id} ===")
        with self.connection.cursor() as cursor:
            cursor.execute("SELECT * FROM users WHERE id = %s", (user_id,))
            result = cursor.fetchone()
            print(f"get_user_by_id result: {result}")
            user = self._unpack_user(result)
        return user


manager = DBManager()
manager.create_users_table()
