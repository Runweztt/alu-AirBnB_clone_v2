#!/usr/bin/python3
"""Defines the State model."""

import os

from sqlalchemy import Column, String
from sqlalchemy.orm import relationship

from models.base_model import Base, BaseModel


class State(BaseModel, Base):
    """Represent a geographical state."""

    __tablename__ = "states"

    name = Column(
        String(128),
        nullable=False
    )

    if os.getenv("HBNB_TYPE_STORAGE") == "db":
        cities = relationship(
            "City",
            backref="state",
            cascade="all, delete-orphan"
        )
    else:
        @property
        def cities(self):
            """Return cities belonging to this state."""
            from models import storage
            from models.city import City

            return [
                city
                for city in storage.all(City).values()
                if city.state_id == self.id
            ]
