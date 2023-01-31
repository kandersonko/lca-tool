from flask import Flask, request
from register import handle_register
from login import handle_login

app = Flask(__name__)

@app.route("/register", methods=['GET', 'POST'])
def register():
    return handle_register()
    #return "<h1>Register</h1>"

@app.route("/login", methods=['GET', 'POST'])
def login():
    return handle_login()
    

@app.route("/")
def index():
    return "<h1>Welcome Page</h1>"
