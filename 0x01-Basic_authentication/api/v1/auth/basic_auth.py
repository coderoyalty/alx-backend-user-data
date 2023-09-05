#!/usr/bin/env python3
"""
BasicAuth module
"""
from .auth import Auth


class BasicAuth(Auth):
    """
    Basic Authentication implementation
    """

    def extract_base64_authorization_header(self, authorization_header: str)\
            -> str:
        """
        returns the base64 part of the "Authorization" header
        """
        if authorization_header is None:
            return None
        if type(authorization_header) is not str:
            return None
        splits = authorization_header.split(' ')
        if len(splits) != 2 or splits[0] != "Basic":
            return None
        return splits[-1]
