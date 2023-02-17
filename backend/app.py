from flask import Flask
from logging.config import dictConfig
import logging

from backend import auth, home, config

dictConfig(
    {
        "version": 1,
        "formatters": {
            "default": {
                "format": "[%(asctime)s] %(levelname)s in %(module)s: %(message)s",
            }
        },
        "handlers": {
            "wsgi": {"class": "logging.StreamHandler", "formatter": "default"}
        },
        "root": {"level": "DEBUG", "handlers": ["wsgi"]},
    }
)


app = Flask(__name__, static_folder="static")
app.config.from_mapping(**config.config)
app.register_blueprint(auth.bp)
app.register_blueprint(home.bp)

app.add_url_rule("/", endpoint="index")

# app.logger.addHandler(logging.StreamHandler())
# app.logger.setLevel(logging.DEBUG)

if __name__ == "__main__":
    app.run()
