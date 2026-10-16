#!/usr/bin/python3
"""Defines the Review model."""

from sqlalchemy import Column, ForeignKey, String

from models.base_model import Base, BaseModel


class Review(BaseModel, Base):
    """Represent a review associated with a place."""

    __tablename__ = "reviews"

    text = Column(
        String(1024),
        nullable=False
    )

    place_id = Column(
        String(60),
        ForeignKey("places.id"),
        nullable=False
    )

    user_id = Column(
        String(60),
        ForeignKey("users.id"),
        nullable=False
    )
