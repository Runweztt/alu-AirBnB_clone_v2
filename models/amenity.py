#!/usr/bin/python3
"""Defines the Amenity model."""

import os

from sqlalchemy import Column, String
from sqlalchemy.orm import relationship

from models.base_model import Base, BaseModel


class Amenity(BaseModel, Base):
    """Represent an amenity available at a place."""

    __tablename__ = "amenities"

    name = Column(
        String(128),
        nullable=False
    )

    if os.getenv("HBNB_TYPE_STORAGE") == "db":
        place_amenities = relationship(
            "Place",
            secondary="place_amenity",
            viewonly=False,
            back_populates="amenities"
        )
