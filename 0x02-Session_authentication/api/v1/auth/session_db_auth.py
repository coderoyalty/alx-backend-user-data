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

        UserSession.load_from_file()
        sessions = UserSession.search({"session_id": session_id})

        if sessions is None or len(sessions) == 0:
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
        try:
            user = users[0]
            user.remove()
            UserSession.save_to_file()
        except Exception:
            return False
        return True
