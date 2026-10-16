#!/usr/bin/python3
"""Defines JSON-backed FileStorage for AirBnB objects."""

import json
import os

from models.amenity import Amenity
from models.base_model import BaseModel
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User


class FileStorage:
    """Serialize model objects to and from a JSON file."""

    __file_path = "file.json"
    __objects = {}

    classes = {
        "Amenity": Amenity,
        "BaseModel": BaseModel,
        "City": City,
        "Place": Place,
        "Review": Review,
        "State": State,
        "User": User
    }

    def all(self, cls=None):
        """Return all objects or only objects of one class."""
        if cls is None:
            return self.__objects

        if isinstance(cls, str):
            cls = self.classes.get(cls)

        if cls is None:
            return {}

        return {
            key: obj
            for key, obj in self.__objects.items()
            if isinstance(obj, cls)
        }

    def new(self, obj):
        """Add an object to the in-memory dictionary."""
        if obj is None:
            return

        key = "{}.{}".format(
            obj.__class__.__name__,
            obj.id
        )

        self.__objects[key] = obj

    def save(self):
        """Serialize all objects to the JSON storage file."""
        serializable = {
            key: obj.to_dict()
            for key, obj in self.__objects.items()
        }

        with open(
            self.__file_path,
            "w",
            encoding="utf-8"
        ) as file:
            json.dump(serializable, file)

    def reload(self):
        """Load objects from the JSON storage file."""
        if not os.path.exists(self.__file_path):
            return

        try:
            with open(
                self.__file_path,
                "r",
                encoding="utf-8"
            ) as file:
                data = json.load(file)

            for key, value in data.items():
                class_name = value.get("__class__")
                model_class = self.classes.get(class_name)

                if model_class is not None:
                    self.__objects[key] = model_class(**value)

        except (json.JSONDecodeError, OSError):
            pass

    def delete(self, obj=None):
        """Delete an object from FileStorage when present."""
        if obj is None:
            return

        key = "{}.{}".format(
            obj.__class__.__name__,
            obj.id
        )

        if key in self.__objects:
            del self.__objects[key]

    def close(self):
        """Reload stored objects from disk."""
        self.reload()
