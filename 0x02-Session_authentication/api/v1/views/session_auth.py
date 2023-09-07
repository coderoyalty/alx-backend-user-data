#!/usr/bin/env python3
"""
flask view that handles all route
for session authentication
"""
from api.v1.views import app_views
from flask import abort, request, jsonify
from models.user import User
from os import getenv


@app_views.route('/auth_session/login', methods=["POST"], strict_slashes=False)
def post_login():
    """
    route handler
    """
    from api.v1.app import auth
    # expected form data
    email = request.form.get('email')
    password = request.form.get('password')

    # form validation

    if not email or email == "":
        return jsonify({"error": "email missing"}), 400
    if not password or len(password) == 0:
        return jsonify({"error": "password missing"}), 400

    # database query
    users = User.search({"email": email})

    if len(users) == 0:
        return jsonify({
            "error": "no user found for this email"
        }), 404

    user = users[0]

    if not user.is_valid_password(password):
        return jsonify({
            "error": "wrong password"
        }), 401

    # create a session and response
    session_id = auth.create_session(user.id)
    res = jsonify(user.to_json())

    # set session in cookie
    session_name = getenv('SESSION_NAME')
    res.set_cookie(session_name, session_id)
    return res


@app_views.delete('/auth_session/logout', strict_slashes=False)
def delete_logout():
    """
    delete a session for the currently authenticated user
    """
    from api.v1.app import auth

    if not auth.destroy_session(request):
        abort(404)

    return jsonify({})
