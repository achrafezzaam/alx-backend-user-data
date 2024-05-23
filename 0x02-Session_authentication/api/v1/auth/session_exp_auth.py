#!/usr/bin/env python3
''' Define the SessionExpAuth class '''
import os
from .session_auth import SessionAuth
from datetime import datetime, timedelta


class SessionExpAuth(SessionAuth):
    ''' Create the SessionExpAuth Object '''
    def __init__(self):
        ''' Instantiate the SessionExpAuth Object '''
        try:
            self.session_duration = int(os.getenv('SESSION_DURATION'))
        except Exception as e:
            self.session_duration = 0

    def create_session(self, user_id=None):
        ''' Create a session ID '''
        try:
            session_id = super().create_session(user_id)
        except Exception as e:
            return None
        self.user_id_by_session_id[session_id] = {
            'user_id': user_id,
            'created_at': datetime.now(),
        }
        return session_id

    def user_id_for_session_id(self, session_id=None):
        ''' Return the user by it's id '''
        if session_id in self.user_id_by_session_id:
            session = self.user_id_by_session_id[session_id]
            if self.session_duration < 1:
                return session['user_id']
            if 'created_at' not in session:
                return None
            now = datetime.now()
            time_delta = timedelta(seconds=self.session_duration)
            expire = session['created_at'] + time_delta
            if expire < now:
                return None
            return session['user_id']
