import logging
from flask import Flask
from mysql.connector import connect, pooling, Error


connection_pool = None

db_config = {
    "host": "db",
    "database": "lca",
    "user": "root",
    "auth_plugin": "mysql_native_password",
}


def create_connection_pool(password_file, pool_size=20, pool_name="db_pool", **kwargs):
    pf = open(password_file, "r")
    password = pf.read().strip()
    pf.close()
    return pooling.MySQLConnectionPool(
        password=password, pool_size=pool_size, pool_name=pool_name, **kwargs
    )


def db_connection(password_file="/run/secrets/db-password"):
    global connection_pool

    connection = None

    if connection_pool is not None:
        try:
            connection = connection_pool.get_connection()
        except Error as e:
            logging.warning(e)
            connection_pool = create_connection_pool(password_file, **db_config)
            connection = connection_pool.get_connection()

    else:
        try:
            connection_pool = create_connection_pool(password_file, **db_config)
            connection = connection_pool.get_connection()
        except Error as e:
            logging.debug(f"==== Connection error: {e} ====")

    return connection


class DBManager:
    def __init__(self):
        db_connection()

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

    def create_user(self, first_name, last_name, email, password_hash, affiliation):
        connection = db_connection()
        if connection:
            with connection.cursor(buffered=True) as cursor:
                try:
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
                    connection.commit()

                except Error as e:
                    # The email was already taken, which caused the
                    # commit to fail. Show a validation error.
                    logging.debug(f"Failed to register user: {e} ===")

        return self.get_user_by_email(email)

    def get_user_by_email(self, email):
        user = None
        connection = db_connection()
        if connection:
            with connection.cursor(buffered=True) as cursor:
                cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
                result = cursor.fetchone()
                user = self._unpack_user(result)
                logging.debug(f"get_user_by_id result: {result}")
                logging.debug(f"=== FOUND user: {user} ===")

        return user

    def get_user_by_id(self, user_id):
        user = None
        logging.debug(f"=== Retrieving user by user_id: {user_id} ===")
        connection = db_connection()
        if connection:
            with connection.cursor(buffered=True) as cursor:
                cursor.execute("SELECT * FROM users WHERE id = %s", (user_id,))
                result = cursor.fetchone()
                logging.debug(f"=== get_user_by_id result: {result}")
                user = self._unpack_user(result)
        return user


manager = DBManager()
# manager.create_users_table()
