from flask import request

def handle_register():
    if request.method == 'GET':
        return "<h1>Registration page</h1>"
    else:
        return "Unauthorized"
