#!/usr/bin/env python3
"""
auth module
"""
import bcrypt
from db import DB
from user import User
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.orm.exc import NoResultFound
import uuid


def _hash_password(password: str) -> bytes:
    """
    hash a password
    """
    encoded = password.encode('utf-8')
    hashed_password = bcrypt.hashpw(
        encoded, bcrypt.gensalt(12)
    )
    return hashed_password


def _generate_uuid() -> str:
    """
    generate a uuid v4.
    """
    uid = uuid.uuid4()
    return str(uid)


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """
        register user
        """
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            hash = _hash_password(password)
            user = self._db.add_user(email, hash)
            return user
        else:
            raise ValueError(f"User {email} already exists")

    def valid_login(self, email: str, password: str) -> bool:
        """
        validate provided credentials
        """
        try:
            user = self._db.find_user_by(email=email)
            hashed = user.hashed_password
            return bcrypt.checkpw(password.encode(), hashed)
        except BaseException:
            return False

    def create_session(self, email: str) -> str:
        """
        create a session for a user
        """
        try:
            user = self._db.find_user_by(email=email)
            uid = _generate_uuid()
            self._db.update_user(user.id, session_id=uid)
        except NoResultFound:
            return None
        return uid

    def get_user_from_session_id(self, session_id: str) -> User:
        """
        fetch user by session id
        """
        if not session_id:
            return None

        try:
            user = self._db.find_user_by(session_id=session_id)
            return user
        except NoResultFound:
            return None

    def destroy_session(self, user_id: int) -> None:
        """
        destroys a user session
        """
        try:
            self._db.update_user(user_id, session_id=None)
        except Exception:
            return None

        return None

    def get_reset_password_token(self, email: str) -> str:
        """
        generate password reset token
        """
        user = self._db.find_user_by(email=email)
        if not user:
            raise ValueError
        token = _generate_uuid()
        self._db.update_user(user.id, reset_token=token)

        return token
