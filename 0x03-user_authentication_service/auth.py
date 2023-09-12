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
