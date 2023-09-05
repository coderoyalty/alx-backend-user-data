#!/usr/bin/env python3
"""
Auth module
"""
from flask import request
from typing import List, TypeVar


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

        if path not in excluded_paths:
            return True

        return False

    def authorization_header(self, request=None) -> str:
        """authorization header"""
        if request is None:
            return None
        return request.headers.get("Authorization", None)

    def current_user(self, request=None) -> TypeVar('User'):
        """return the current user"""
        return None
