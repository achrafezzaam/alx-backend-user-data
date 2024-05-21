#!/usr/bin/env python3
''' Define the BasicAuth class '''
from .auth import Auth
import base64
from models.user import User
from typing import TypeVar


class BasicAuth(Auth):
    ''' Create the BasicAuth Object '''
    def extract_base64_authorization_header(
            self, authorization_header: str) -> str:
        """ Return the Base64 part of the Authorization header
        """
        if authorization_header is None or\
           not isinstance(authorization_header, str) or\
           authorization_header.split()[0] != 'Basic':
            return None
        return authorization_header.split()[1]

    def decode_base64_authorization_header(
            self, base64_authorization_header: str) -> str:
        """ Return the decoded value of a Base64 string
            base64_authorization_header
        """
        if base64_authorization_header is None or\
           not isinstance(base64_authorization_header, str):
            return None
        try:
            return base64.b64decode(base64_authorization_header)\
                    .decode('utf-8')
        except Exception as e:
            return None

    def extract_user_credentials(
            self, decoded_base64_authorization_header: str) -> (str, str):
        """ Return the user email and password from
            the Base64 decoded value"""
        if not isinstance(decoded_base64_authorization_header, str):
            search = r'(?P<usr>[^:]+):(?P<pwd>.+)'
            info_match = re.fullmatch(
                    search,
                    decoded_base64_authorization_header.strip()
                    )
            if info_match is not None:
                usr = info_match.group('usr')
                pwd = info_match.group('pwd')
            return usr, pwd
        return None, None

    def user_object_from_credentials(
            self, user_email: str, user_pwd: str) -> TypeVar('User'):
        """ Returns the User instance based on his email and password
        """
        if user_email is None or user_pwd is None or\
                not isinstance(user_email, str) or\
                not isinstance(user_pwd, str):
            return None
        try:
            users = User.search({'email': user_email})
        except Exception as e:
            return None
        if len(users) < 1:
            return None
        if users[0].is_valid_password(user_pwd):
            return users[0]
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """ Overloads Auth and retrieves the User instance for a request
        """
        header = self.authorization_header(request)
        b64_auth_token = self.extract_base64_authorization_header(header)
        auth_token = self.decode_base64_authorization_header(b64_auth_token)
        mail, pwd = self.extract_user_credentials(auth_token)
        return self.user_object_from_credentials(mail, pwd)
