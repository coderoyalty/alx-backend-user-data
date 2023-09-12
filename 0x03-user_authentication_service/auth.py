#!/usr/bin/env python3
"""
auth module
"""
import bcrypt


def _hash_password(password: str) -> bytes:
    """
    hash a password
    """
    encoded = password.encode('utf-8')
    hashed_password = bcrypt.hashpw(
        encoded, bcrypt.gensalt(12)
    )
    return hashed_password
