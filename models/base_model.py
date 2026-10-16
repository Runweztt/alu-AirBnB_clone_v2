#!/usr/bin/python3
"""Defines the common base model for all AirBnB objects."""

import uuid
from datetime import datetime

from sqlalchemy import Column, DateTime, String
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class BaseModel:
    """Provide common identifiers, timestamps and storage methods."""

    id = Column(
        String(60),
        nullable=False,
        primary_key=True
    )

    created_at = Column(
        DateTime,
        nullable=False,
        default=datetime.utcnow
    )

    updated_at = Column(
        DateTime,
        nullable=False,
        default=datetime.utcnow
    )

    def __init__(self, *args, **kwargs):
        """Initialize a new model from optional keyword arguments."""
        for key, value in kwargs.items():
            if key == "__class__":
                continue

            if key in ("created_at", "updated_at"):
                if isinstance(value, str):
                    value = datetime.fromisoformat(value)

            setattr(self, key, value)

        if "id" not in kwargs:
            self.id = str(uuid.uuid4())

        if "created_at" not in kwargs:
            self.created_at = datetime.utcnow()

        if "updated_at" not in kwargs:
            self.updated_at = datetime.utcnow()

    def __str__(self):
        """Return the standard printable representation."""
        return "[{}] ({}) {}".format(
            self.__class__.__name__,
            self.id,
            self.__dict__
        )

    def save(self):
        """Update the timestamp and persist this object."""
        from models import storage

        self.updated_at = datetime.utcnow()
        storage.new(self)
        storage.save()

    def to_dict(self):
        """Return a serializable dictionary representation."""
        result = self.__dict__.copy()
        result.pop("_sa_instance_state", None)

        for key in ("created_at", "updated_at"):
            value = result.get(key)

            if isinstance(value, datetime):
                result[key] = value.isoformat()

        result["__class__"] = self.__class__.__name__
        return result

    def delete(self):
        """Remove this object from the active storage engine."""
        from models import storage

        storage.delete(self)
