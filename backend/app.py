from flask import Flask
# from flask.logging import default_handler
# import logging

from backend import auth, home


app = Flask(__name__) 
app.config.from_mapping(
    SECRET_KEY="dev-secret-3aerq23raea3083qa"
)
app.register_blueprint(auth.bp)
app.register_blueprint(home.bp)

app.add_url_rule("/", endpoint="index")

# app.logger.addHandler(default_handler)
# app.logger.addHandler(logging.getLogger())

if __name__ == '__main__':
    app.run()
