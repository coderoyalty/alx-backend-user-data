#!/usr/bin/env python3
"""
Session Authentication
"""
from api.v1.auth.auth import Auth
from uuid import uuid4
from models.user import User


class SessionAuth(Auth):
    """
    Session Authentication Implementation
    """
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """
        create a session id for a user id
        """
        if user_id is None:
            return None
        if type(user_id) is not str:
            return None
        session_id = str(uuid4())
        self.user_id_by_session_id[session_id] = user_id
        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """
        get user id based on a session id
        """
        if session_id is None or not isinstance(session_id, str):
            return None

        return self.user_id_by_session_id.get(session_id)

    def current_user(self, request=None):
        """
        overload Auth.current_user
        """
        try:
            session_id = self.session_cookie(request)
            user_id = self.user_id_for_session_id(session_id)
            user = User.get(user_id)
        except Exception:
            return None

        return user

    def destroy_session(self, request=None):
        """
        logout a session
        """

        session_id = self.session_cookie(request)
        if session_id is None:
            return False
        user_id = self.user_id_for_session_id(session_id)
        if user_id is None:
            return False
        self.user_id_by_session_id.pop(session_id)
        return True
