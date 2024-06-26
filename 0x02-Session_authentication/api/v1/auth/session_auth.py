#!/usr/bin/env python3
''' Define the SessionAuth class '''
from .auth import Auth
from uuid import uuid4
from models.user import User


class SessionAuth(Auth):
    ''' Create the SessionAuth Object '''
    user_id_by_session_id = dict()

    def create_session(self, user_id: str = None) -> str:
        ''' Create a session id '''
        if user_id is None or not isinstance(user_id, str):
            return None
        session_id = str(uuid4())
        self.user_id_by_session_id[session_id] = user_id
        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        ''' Return a User ID based on a Session ID '''
        if session_id is None or not isinstance(session_id, str):
            return None
        return self.user_id_by_session_id.get(session_id)

    def current_user(self, request=None):
        ''' Return the current user '''
        user_id = self.user_id_for_session_id(self.session_cookie(request))
        return User.get(user_id)

    def destroy_session(self, request=None):
        ''' Terminate the current user session '''
        session_id = self.session_cookie(request)
        user_id = self.user_id_for_session_id(session_id)
        if request is None or session_id is None or user_id is None:
            return False
        del self.user_id_by_session_id[session_id]
        return True
