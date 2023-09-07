#!/usr/bin/env python3
"""
session authentication with expiration date
"""
from datetime import datetime, timedelta
from .session_auth import SessionAuth
from os import getenv


class SessionExpAuth(SessionAuth):
    """
    add expiration date to session auth
    """

    def __init__(self):
        """initialize
        """
        super().__init__()
        try:
            self.session_duration = int(getenv('SESSION_DURATION'))
        except Exception:
            self.session_duration = 0

    def create_session(self, user_id=None):
        """
        create session
        """
        session_id = super().create_session(user_id)
        if not session_id:
            return session_id
        session_dict = {
            "user_id": user_id,
            "created_at": datetime.now()
        }
        self.user_id_by_session_id[session_id] = session_dict
        return session_id

    def user_id_for_session_id(self, session_id=None):
        """
        gets the user id for session
        """
        if not session_id:
            return None
        if session_id not in self.user_id_by_session_id.keys():
            return None
        session_dict = self.user_id_by_session_id.get(session_id)
        if session_dict is None:
            return None

        if self.session_duration <= 0:
            return session_dict.get('user_id')

        created_at = session_dict.get('created_at')
        if created_at is None:
            return None

        expired = created_at + timedelta(seconds=self.session_duration)
        if expired < datetime.now():
            return None
        return session_dict.get('user_id')
