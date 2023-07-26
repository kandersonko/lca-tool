import logging
from pathlib import Path
import os
from uuid import uuid4
from flask import Flask, g
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


def db_connection(password_file):
    global connection_pool

    connection = None

    if connection_pool is not None:
        try:
            connection = connection_pool.get_connection()
        except Error as e:
            logging.warning(e)
            connection_pool = create_connection_pool(
                password_file, **db_config)
            connection = connection_pool.get_connection()

    else:
        try:
            connection_pool = create_connection_pool(
                password_file, **db_config)
            connection = connection_pool.get_connection()
        except Error as e:
            logging.debug(f"==== Connection error: {e} ====")

    return connection


# Use singleton pattern
class DBManager(object):
    _instance = None
    password_file = None

    def __init__(self):
        raise RuntimeError("Call instance() instead")

    @classmethod
    def instance(cls, password_file):
        if cls._instance is None:
            print("Creating new instance")
            cls._instance = cls.__new__(cls)
            # Put any initialization here.
            cls._instance.password_file = password_file
            db_connection(password_file)
        return cls._instance

    def _unpack_user(self, query_result):
        if query_result is None:
            return None
        (
            user_id,
            first_name,
            last_name,
            email,
            password,
            affiliation,
            status,
            plan_id,
            created_at,
            updated_at,
            last_login,
        ) = query_result
        user = {
            "id": user_id,
            "first_name": first_name,
            "last_name": last_name,
            "email": email,
            "password": password,
            "affiliation": affiliation,
            "status": status,
            "plan_id": plan_id,
            "created_at": created_at,
            "updated_at": updated_at,
            "last_login": last_login,
        }
        return user

    def create_user(self, first_name, last_name, email, password_hash, affiliation):
        connection = db_connection(self.password_file)
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
        connection = db_connection(self.password_file)
        if connection:
            with connection.cursor(buffered=True) as cursor:
                cursor.execute(
                    "SELECT * FROM users WHERE email = %s", (email,))
                result = cursor.fetchone()
                user = self._unpack_user(result)
                # logging.debug(f"get_user_by_id result: {result}")
                # logging.debug(f"=== FOUND user: {user} ===")
                if user:
                    user = self.update_user_last_login(user["id"])

        return user

    def get_user_by_id(self, user_id):
        user = None
        # logging.debug(f"=== Retrieving user by user_id: {user_id} ===")
        connection = db_connection(self.password_file)
        if connection:
            with connection.cursor(buffered=True) as cursor:
                cursor.execute("SELECT * FROM users WHERE id = %s", (user_id,))
                result = cursor.fetchone()
                # logging.debug(f"=== get_user_by_id result: {result}")
                user = self._unpack_user(result)
        return user

    def get_plan_by_user_id(self, user_id):
        logging.error(f"=== Retrieving plan by user_id: {user_id} ===")
        plan = None
        connection = db_connection(self.password_file)
        if connection:
            with connection.cursor(buffered=True) as cursor:
                cursor.execute("""
                SELECT plans.id, plans.tier, plans.storage_url FROM users
                INNER JOIN plans ON users.id = plans.id
                WHERE users.id=%s
                """, (user_id,))
                result = cursor.fetchone()
                (id, tier, storage_url) = result
                plan = dict(id=id, tier=tier, storage_url=storage_url)
                logging.debug(f"=== get_plan_by_user_id result: {result}")
        return plan

    def update_user_last_login(self, user_id):
        user = None
        # logging.debug(
        #     f"=== Updating last_login_on for user with id : {user_id} ===")
        connection = db_connection(self.password_file)
        if connection:
            with connection.cursor(buffered=True) as cursor:
                cursor.execute(
                    """
                    UPDATE users SET last_login=NOW()
                    WHERE id=%s
                    """,
                    (user_id,),
                )
                connection.commit()
                user = self.get_user_by_id(user_id)
        return user

    def create_user_plan(self, user_id, tier):
        # logging.debug(
        #     f"=== Creating plan {tier} for user with id : {user_id} ===")
        plan_prices = {"free": 0.0, "premium": 200.0, "enterprise": 500.0}
        price = plan_prices.get(tier)
        storage_url = str(uuid4())

        connection = db_connection(self.password_file)
        if connection:
            with connection.cursor(buffered=True) as cursor:
                try:
                    connection.start_transaction()
                    cursor.execute(
                        """
                        INSERT INTO plans (tier, price, storage_url) VALUES (%s, %s, %s);
                    """,
                        (
                            tier,
                            price,
                            storage_url,
                        ),
                    )
                    # Get the ID of the newly inserted plan
                    plan_id = cursor.lastrowid

                    # Define the SQL query to update the user's plan_id with the new plan_id
                    update_query = """
                        UPDATE users
                        SET plan_id = %s
                        WHERE id = %s;
                    """

                    # Execute the update query with the new plan_id and user_id
                    cursor.execute(update_query, (plan_id, user_id))

                    connection.commit()
                    storage_path = Path("data/" + storage_url)
                    os.makedirs(storage_path)
                    # logging.debug(
                    #     f"=== Created plan:  {tier}, {price}, {user_id}, {storage_url}"
                    # )

                except Error as e:
                    logging.debug(f"=== Error creating plan: {e}")
                    connection.rollback()

    def activate_user(self, email):
        # logging.debug(f"=== Activating user with email : {email} ===")
        user = None
        connection = db_connection(self.password_file)
        if connection:
            with connection.cursor(buffered=True) as cursor:
                cursor.execute(
                    """
                    UPDATE users SET status='active'
                    WHERE email=%s
                    """,
                    (email,),
                )
                connection.commit()
                user = self.get_user_by_email(email)
        return user

    def reset_password(self, email, new_password_hash):
        user = None
        connection = db_connection(self.password_file)
        if connection:
            with connection.cursor(buffered=True) as cursor:
                cursor.execute(
                    """
                    UPDATE users SET password=%s, status='inactive'
                    WHERE email=%s
                    """,
                    (new_password_hash, email),
                )
                connection.commit()
                user = self.get_user_by_email(email)
        return user

    def set_user_status(self, email, status):
        user = None
        connection = db_connection(self.password_file)
        if connection:
            with connection.cursor(buffered=True) as cursor:
                cursor.execute(
                    """
                    UPDATE users SET status=%s
                    WHERE email=%s
                    """,
                    (status, email),
                )
                connection.commit()
                user = self.get_user_by_email(email)
        return user
