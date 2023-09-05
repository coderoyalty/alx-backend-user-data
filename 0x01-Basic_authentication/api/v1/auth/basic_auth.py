#!/usr/bin/env python3
"""
BasicAuth module
"""
from .auth import Auth
import base64


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

    def decode_base64_authorization_header(
            self, base64_authorization_header: str) -> str:
        """
        decode a base64 authorization header
        """
        if base64_authorization_header is None:
            return None
        if type(base64_authorization_header) is not str:
            return None
        try:
            encoded = base64_authorization_header.encode('utf-8')
            decoded_bytes = base64.b64decode(encoded)
            return decoded_bytes.decode('utf-8')
        except BaseException:
            return None

    def extract_user_credentials(
            self, decoded_base64_authorization_header: str
    ) -> (str, str):
        """
        extract user credentials from the decoded authorization
        header
        """
        if decoded_base64_authorization_header is None:
            return (None, None)
        if type(decoded_base64_authorization_header) is not str:
            return (None, None)
        user_password = decoded_base64_authorization_header.split(':')
        if len(user_password) != 2:
            return (None, None)
        return tuple(user_password)
