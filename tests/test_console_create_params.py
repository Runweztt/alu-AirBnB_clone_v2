#!/usr/bin/python3
"""Tests the parameter-aware create console command."""

import os
import unittest
from io import StringIO
from unittest.mock import patch

from console import HBNBCommand
from models import storage
from models.place import Place
from models.state import State


@unittest.skipIf(
    os.getenv("HBNB_TYPE_STORAGE") == "db",
    "FileStorage-specific create parameter tests"
)
class TestCreateParameters(unittest.TestCase):
    """Validate typed parameters passed to create."""

    def setUp(self):
        """Clear FileStorage before each test."""
        storage.all().clear()

    def tearDown(self):
        """Clear FileStorage and remove generated JSON."""
        storage.all().clear()

        if os.path.exists("file.json"):
            os.remove("file.json")

    def test_create_string_parameter(self):
        """Create should convert underscores in strings to spaces."""
        command = HBNBCommand()

        with patch(
            "sys.stdout",
            new=StringIO()
        ):
            command.do_create(
                'State name="New_York"'
            )

        states = list(
            storage.all(State).values()
        )

        self.assertEqual(len(states), 1)
        self.assertEqual(
            states[0].name,
            "New York"
        )

    def test_create_numeric_parameters(self):
        """Create should preserve integer and float types."""
        command = HBNBCommand()

        with patch(
            "sys.stdout",
            new=StringIO()
        ):
            command.do_create(
                'Place city_id="1" user_id="2" '
                'name="My_house" number_rooms=4 '
                'latitude=37.5'
            )

        places = list(
            storage.all(Place).values()
        )

        self.assertEqual(len(places), 1)
        self.assertEqual(
            places[0].number_rooms,
            4
        )
        self.assertIsInstance(
            places[0].number_rooms,
            int
        )
        self.assertEqual(
            places[0].latitude,
            37.5
        )
        self.assertIsInstance(
            places[0].latitude,
            float
        )


if __name__ == "__main__":
    unittest.main()
