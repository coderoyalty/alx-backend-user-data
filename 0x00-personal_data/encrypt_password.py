#!/usr/bin/env python3
"""
encrypt password
"""
import bcrypt


def hash_password(password: str) -> bytes:
    """hash `password`"""
    password = password.encode()
    hashed = bcrypt.hashpw(password, bcrypt.gensalt())
    return hashed


def is_valid(hashed_password: bytes, password: str) -> bool:
    """check if a hashed password is a string password is valid"""
    return bcrypt.checkpw(str(password).encode(), hashed_password)
