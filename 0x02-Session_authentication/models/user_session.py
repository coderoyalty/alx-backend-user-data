#!/usr/bin/env python3
"""
session in database, rather than memory
"""
from .base import Base


class UserSession(Base):
    """Session model"""

    def __init__(self, *args: list, **kwargs: dict):
        """initialize
        """
        super().__init__(*args, **kwargs)
        self.user_id = kwargs.get("user_id")
        self.session_id = kwargs.get("session_id")
