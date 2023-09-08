#!/usr/bin/env python3
"""
session db auth
"""
from .session_exp_auth import SessionExpAuth
from models.user_session import UserSession
from datetime import datetime, timedelta


class SessionDBAuth(SessionExpAuth):
    """
    Session Auth that saves to database
    """

    def __init__(self):
        """initialize
        """
        super().__init__()
        UserSession.load_from_file()

    def create_session(self, user_id=None):
        """create a session"""
        session_id = super().create_session(user_id)
        if not session_id:
            return None

        data = {
            "user_id": user_id,
            "session_id": session_id
        }

        session = UserSession(**data)
        session.save()

        return session_id

    def user_id_for_session_id(self, session_id=None):
        """
        get user id based on a session
        """
        if not session_id:
            return None

        sessions = UserSession.search({"session_id": session_id})

        if sessions is None:
            return None

        session = sessions[0]

        duration = timedelta(seconds=self.session_duration)
        expired = session.created_at + duration

        if expired < datetime.now():
            return None

        return session.user_id

    def destroy_session(self, request=None):
        """
        destroy a session
        """
        session_id = self.session_cookie(request)
        if not session_id:
            return False
        user_id = self.user_id_for_session_id(session_id)
        if not user_id:
            return False

        users = UserSession.search({'session_id': session_id})

        if not users:
            return False
        user = users[0]
        try:
            user.remove()
            UserSession.save_to_file()
        except Exception:
            return False
        return True
