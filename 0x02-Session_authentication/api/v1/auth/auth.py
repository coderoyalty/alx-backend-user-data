#!/usr/bin/env python3
"""
Auth module
"""
from flask import request
from typing import List, TypeVar
from os import getenv


class Auth:
    """ API authentication manager """

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """ require auth
        """
        if path is None or excluded_paths is None:
            return True
        if len(excluded_paths) == 0:
            return True

        if path[-1] != '/':
            path = f"{path}/"

        if path in excluded_paths:
            return False
        for exc in excluded_paths:
            length = len(exc)
            if length == 0:
                continue
            if exc[:-1] == path[: length - 1]:
                return False
        return True

    def authorization_header(self, request=None) -> str:
        """authorization header"""
        if request is None:
            return None
        return request.headers.get("Authorization", None)

    def current_user(self, request=None) -> TypeVar('User'):
        """return the current user"""
        return None

    def session_cookie(self, request=None):
        """
        returns a cookie value from the request
        """
        if request is None:
            return None

        session_name = getenv('SESSION_NAME')
        return request.cookies.get(session_name)
