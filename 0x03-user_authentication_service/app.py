#!/usr/bin/env python3
"""
basic flask app
"""
from flask import Flask, jsonify, request, abort
from auth import Auth


app = Flask(__name__)
AUTH = Auth()


@app.route('/', methods=['GET'], strict_slashes=False)
def root_get():
    """
    GET - route /
    """
    return jsonify({
        "message": "Bienvenue"
    })


@app.route('/users', methods=['POST'], strict_slashes=False)
def users():
    """
    POST - /users
    create a user with the given credentials
    """
    email = request.form.get('email')
    password = request.form.get('password')

    try:
        user = AUTH.register_user(email, password)
    except ValueError:
        return jsonify({
            "message": "email already registered"
        }), 400

    return jsonify({
        "email": user.email, "message": "user created"
    }), 200


@app.route('/sessions', strict_slashes=False, methods=["POST"])
def login():
    """
    POST /sessions
    """
    form = request.form
    email = form.get('email')
    password = form.get('password')
    if not AUTH.valid_login(email, password):
        return abort(401)
    session_id = AUTH.create_session(email)
    response = jsonify({
        "email": email, "message": "logged in"
    })

    response.set_cookie("session_id", session_id)
    return response


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
