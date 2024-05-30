#!/usr/bin/env python3
"""DB module
"""
from sqlalchemy import create_engine, tuple_
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.orm.exc import NoResultFound
from user import Base, User


class DB:
    """DB class
    """

    def __init__(self) -> None:
        """Initialize a new DB instance
        """
        self._engine = create_engine("sqlite:///a.db", echo=False)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """Memoized session object
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        """Create a new user
        """
        try:
            user = User(email=email, hashed_password=hashed_password)
            self.__session.add(user)
            self.__session.commit()
        except Exception as e:
            self._session.rollback()
            user = None
        return user

    def find_user_by(self, **kwargs) -> User:
        """Search for a user in the db given a keyword/value
            arguments combination
        """
        keys, vals = list(), list()
        for key, val in kwargs.items():
            if hasattr(User, key):
                keys.append(getattr(User, key))
                vals.append(val)
            else:
                raise InvalidRequestError()
        user = self._session.query(User).filter(
                tuple_(*keys).in_([tuple(vals)])
                ).first()
        if user is None:
            raise NoResultFound()
        return user

    def update_user(self, user_id: int, **kwargs) -> None:
        """ Update a user's data using keyword/value arguments
        """
        user = self.find_user_by(id=user_id)
        if user is None:
            return
        new = dict()
        for key, val in kwargs.items():
            if hasattr(User, key):
                new[getattr(User, key)] = val
            else:
                raise ValueError()
        self._session.query(User).filter(User.id == user_id).update(
            new,
            synchronize_session=False,
        )
        self._session.commit()
