#!/usr/bin/env python3
''' Handle password encryption '''
import bcrypt


def hash_password(password: str) -> bytes:
    ''' Salt a password hash '''
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())


def is_valid(hashed_password: bytes, password: str) -> bool:
    '''Check if the given password is valid'''
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password)
