#!/usr/bin/python3
"""Defines the Place model and Place-Amenity association."""

import os

from sqlalchemy import (
    Column,
    Float,
    ForeignKey,
    Integer,
    String,
    Table
)
from sqlalchemy.orm import relationship

from models.base_model import Base, BaseModel


place_amenity = Table(
    "place_amenity",
    Base.metadata,
    Column(
        "place_id",
        String(60),
        ForeignKey("places.id"),
        primary_key=True,
        nullable=False
    ),
    Column(
        "amenity_id",
        String(60),
        ForeignKey("amenities.id"),
        primary_key=True,
        nullable=False
    )
)


class Place(BaseModel, Base):
    """Represent a property available for accommodation."""

    __tablename__ = "places"

    city_id = Column(
        String(60),
        ForeignKey("cities.id"),
        nullable=False
    )

    user_id = Column(
        String(60),
        ForeignKey("users.id"),
        nullable=False
    )

    name = Column(
        String(128),
        nullable=False
    )

    description = Column(
        String(1024),
        nullable=True
    )

    number_rooms = Column(
        Integer,
        nullable=False,
        default=0
    )

    number_bathrooms = Column(
        Integer,
        nullable=False,
        default=0
    )

    max_guest = Column(
        Integer,
        nullable=False,
        default=0
    )

    price_by_night = Column(
        Integer,
        nullable=False,
        default=0
    )

    latitude = Column(
        Float,
        nullable=True
    )

    longitude = Column(
        Float,
        nullable=True
    )

    amenity_ids = []

    def __init__(self, *args, **kwargs):
        """Initialize a Place and its FileStorage amenity IDs."""
        super().__init__(*args, **kwargs)

        if os.getenv("HBNB_TYPE_STORAGE") != "db":
            values = kwargs.get("amenity_ids", [])
            self.amenity_ids = list(values)

    if os.getenv("HBNB_TYPE_STORAGE") == "db":
        reviews = relationship(
            "Review",
            backref="place",
            cascade="all, delete-orphan"
        )

        amenities = relationship(
            "Amenity",
            secondary=place_amenity,
            viewonly=False,
            back_populates="place_amenities"
        )
    else:
        @property
        def reviews(self):
            """Return reviews linked to this place."""
            from models import storage
            from models.review import Review

            return [
                review
                for review in storage.all(Review).values()
                if review.place_id == self.id
            ]

        @property
        def amenities(self):
            """Return amenities linked through amenity_ids."""
            from models import storage
            from models.amenity import Amenity

            objects = storage.all(Amenity)

            return [
                amenity
                for amenity in objects.values()
                if amenity.id in self.amenity_ids
            ]

        @amenities.setter
        def amenities(self, obj):
            """Link an Amenity object to this Place."""
            from models.amenity import Amenity

            if isinstance(obj, Amenity):
                if obj.id not in self.amenity_ids:
                    self.amenity_ids.append(obj.id)
