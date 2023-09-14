#!/usr/bin/env python3
""" End-to-end integration test"""

import requests

URL = 'http://localhost:5000'


def register_user(email: str, password: str) -> None:
    """ validate user registration """
    data = {
        "email": email, "password": password
    }
    response = requests.post(f'{URL}/users', data)

    msg = {
        "email": email, "message": "user created"
    }

    assert response.status_code == 200
    assert response.json() == msg


def log_in_wrong_password(email: str, password: str) -> None:
    """ test wrong password login attempt """
    data = {
        "email": email,
        "password": password
    }
    response = requests.post(f'{URL}/sessions', data)

    assert response.status_code == 401


def log_in(email: str, password: str) -> str:
    """ validate successful login """
    data = {
        "email": email,
        "password": password
    }
    response = requests.post(f'{URL}/sessions', data)

    msg = {"email": email, "message": "logged in"}

    assert response.status_code == 200
    assert response.json() == msg

    session_id = response.cookies.get("session_id")

    return session_id


def profile_unlogged() -> None:
    """ test GET /profile while logged-out """
    cookies = {
        "session_id": ""
    }
    response = requests.get(f'{URL}/profile', cookies=cookies)

    assert response.status_code == 403


def profile_logged(session_id: str) -> None:
    """ test GET /profile while logged in """
    cookies = {
        "session_id": session_id
    }
    response = requests.get(f'{URL}/profile', cookies=cookies)

    msg = {"email": EMAIL}

    assert response.status_code == 200
    assert response.json() == msg


def log_out(session_id: str) -> None:
    """ test logout """
    cookies = {
        "session_id": session_id
    }
    response = requests.delete(f'{URL}/sessions', cookies=cookies)

    msg = {"message": "Bienvenue"}

    assert response.status_code == 200
    assert response.json() == msg


def reset_password_token(email: str) -> str:
    """ test reset_token endpoint """
    data = {
        "email": email
    }
    response = requests.post(f'{URL}/reset_password', data)

    assert response.status_code == 200

    reset_token = response.json().get("reset_token")

    msg = {"email": email, "reset_token": reset_token}

    assert response.json() == msg

    return reset_token


def update_password(email: str, reset_token: str, new_password: str) -> None:
    """ test password update """
    data = {
        "email": email,
        "reset_token": reset_token,
        "new_password": new_password
    }
    response = requests.put(f'{URL}/reset_password', data)

    msg = {"email": email, "message": "Password updated"}

    assert response.status_code == 200
    assert response.json() == msg


EMAIL = "guillaume@holberton.io"
PASSWD = "b4l0u"
NEW_PASSWD = "t4rt1fl3tt3"

if __name__ == "__main__":

    register_user(EMAIL, PASSWD)
    log_in_wrong_password(EMAIL, NEW_PASSWD)
    profile_unlogged()
    session_id = log_in(EMAIL, PASSWD)
    profile_logged(session_id)
    log_out(session_id)
    reset_token = reset_password_token(EMAIL)
    update_password(EMAIL, reset_token, NEW_PASSWD)
    log_in(EMAIL, NEW_PASSWD)
