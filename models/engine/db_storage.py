#!/usr/bin/python3
"""Defines the SQLAlchemy database storage engine."""

import os

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

from models.amenity import Amenity
from models.base_model import Base
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User


class DBStorage:
    """Manage persistence using a MySQL database."""

    __engine = None
    __session = None

    classes = {
        "Amenity": Amenity,
        "City": City,
        "Place": Place,
        "Review": Review,
        "State": State,
        "User": User
    }

    def __init__(self):
        """Create the SQLAlchemy engine from environment variables."""
        user = os.getenv("HBNB_MYSQL_USER")
        password = os.getenv("HBNB_MYSQL_PWD")
        host = os.getenv("HBNB_MYSQL_HOST")
        database = os.getenv("HBNB_MYSQL_DB")

        url = "mysql+mysqldb://{}:{}@{}/{}".format(
            user,
            password,
            host,
            database
        )

        self.__engine = create_engine(
            url,
            pool_pre_ping=True
        )

        if os.getenv("HBNB_ENV") == "test":
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """Return database objects as a keyed dictionary."""
        result = {}

        if cls is not None:
            if isinstance(cls, str):
                cls = self.classes.get(cls)

            if cls is None:
                return result

            objects = self.__session.query(cls).all()

            for obj in objects:
                key = "{}.{}".format(
                    obj.__class__.__name__,
                    obj.id
                )
                result[key] = obj

            return result

        for model_class in self.classes.values():
            objects = self.__session.query(model_class).all()

            for obj in objects:
                key = "{}.{}".format(
                    obj.__class__.__name__,
                    obj.id
                )
                result[key] = obj

        return result

    def new(self, obj):
        """Add an object to the current database session."""
        if obj is not None:
            self.__session.add(obj)

    def save(self):
        """Commit all pending database changes."""
        self.__session.commit()

    def delete(self, obj=None):
        """Delete an object from the current session."""
        if obj is not None:
            self.__session.delete(obj)

    def reload(self):
        """Create database tables and a scoped session."""
        Base.metadata.create_all(self.__engine)

        factory = sessionmaker(
            bind=self.__engine,
            expire_on_commit=False
        )

        Session = scoped_session(factory)
        self.__session = Session

    def close(self):
        """Remove the current scoped database session."""
        if self.__session is not None:
            self.__session.remove()
