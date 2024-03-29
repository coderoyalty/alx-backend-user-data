#!/usr/bin/env python3
"""
basic flask app
"""
from flask import (
    Flask, jsonify, request, abort, redirect
)
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


@app.route('/sessions', methods=["DELETE"], strict_slashes=False)
def logout():
    """
    DELETE /sessions
    """
    session_id = request.cookies.get('session_id')
    user = AUTH.get_user_from_session_id(session_id)
    if not user:
        return abort(403)
    AUTH.destroy_session(session_id)
    return redirect('/')


@app.route('/profile', methods=['GET'], strict_slashes=False)
def profile():
    """
    GET - /profile
    """
    session_id = request.cookies.get('session_id')
    user = AUTH.get_user_from_session_id(session_id)
    if not user:
        return abort(403)
    return jsonify({
        "email": user.email
    }), 200


@app.route('/reset_password', methods=["POST"], strict_slashes=False)
def get_reset_password_token():
    """
    reset password token
    """
    email = request.form.get('email')
    try:
        token = AUTH.get_reset_password_token(email)
    except ValueError:
        return abort(403)

    return jsonify({
        "email": email,
        "reset_token": token
    }), 200


@app.route('/reset_password', methods=["PUT"], strict_slashes=False)
def update_password():
    """
    PUT - /reset_password
    """

    try:
        email = request.form.get('email')
        token = request.form.get('reset_token')
        new = request.form.get('new_password')
        AUTH.update_password(token, new)
    except KeyError:
        abort(400)
    except ValueError:
        abort(403)

    return jsonify({
        "email": email,
        "message": "Password updated"
    }), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
