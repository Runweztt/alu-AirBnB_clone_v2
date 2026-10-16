#!/usr/bin/python3
"""Initialize AirBnB models and select the active storage engine."""

import os

from models.amenity import Amenity
from models.base_model import BaseModel
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User


if os.getenv("HBNB_TYPE_STORAGE") == "db":
    from models.engine.db_storage import DBStorage

    storage = DBStorage()
else:
    from models.engine.file_storage import FileStorage

    storage = FileStorage()


storage.reload()


__all__ = [
    "Amenity",
    "BaseModel",
    "City",
    "Place",
    "Review",
    "State",
    "User",
    "storage"
]
