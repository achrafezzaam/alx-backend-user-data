#!/usr/bin/env python3
"""DB module
"""
from sqlalchemy import create_engine
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
        self._engine = create_engine("sqlite:///a.db", echo=True)
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
        user = User(email=email, hashed_password=hashed_password)
        self._session.rollback()
        self.__session.add(user)
        self.__session.commit()
        return user

    def find_user_by(self, **kwargs) -> User:
        """Search for a user in the db given a keyword/value
            arguments combination
        """
        for key, val in kwargs.items():
            if not hasattr(User, key):
                raise InvalidRequestError()
        user = self.__session.query(User).filter_by(**kwargs).first()
        if user is None:
            raise NoResultFound()
        return user

    def update_user(self, user_id: int, **kwargs) -> None:
        """ Update a user's data using keyword/value arguments
        """
        user = self.find_user_by(id=user_id)
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
