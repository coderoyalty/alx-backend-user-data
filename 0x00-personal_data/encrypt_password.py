#!/usr/bin/env python3
"""
encrypt password
"""
import bcrypt


def hash_password(password: str) -> bytes:
    """hash `password`"""
    hashed = bcrypt.hashpw(bytes(password), bcrypt.gensalt())
    return hashed
