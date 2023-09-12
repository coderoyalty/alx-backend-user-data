#!/usr/bin/env python3
"""
basic flask app
"""
from flask import Flask, jsonify, request
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


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
