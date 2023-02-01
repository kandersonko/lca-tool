import os
from flask import Flask

def create_app():
    # Create and configure a Flask app instance
    app = Flask(__name__, instance_relative_config=True)

    app.config.from_mapping(
        SECRET_KEY="dev",
        DATABASE=os.path.join(app.instance_path, "lca_tool.sqlite")
    )

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass # we should log the error later!


    @app.route("/status")
    def status():
        return "<h1>App running!</h1>"


    from lca_tool import home, auth, db

    db.init_app(app)

    app.register_blueprint(auth.bp)
    app.register_blueprint(home.bp)

    app.add_url_rule("/", endpoint="index")


    return app
