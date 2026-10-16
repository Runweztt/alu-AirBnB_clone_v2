#!/usr/bin/python3
"""Defines the City model."""

import os

from sqlalchemy import Column, ForeignKey, String
from sqlalchemy.orm import relationship

from models.base_model import Base, BaseModel


class City(BaseModel, Base):
    """Represent a city belonging to a state."""

    __tablename__ = "cities"

    name = Column(
        String(128),
        nullable=False
    )

    state_id = Column(
        String(60),
        ForeignKey("states.id"),
        nullable=False
    )

    if os.getenv("HBNB_TYPE_STORAGE") == "db":
        places = relationship(
            "Place",
            backref="cities",
            cascade="all, delete-orphan"
        )
