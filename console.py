#!/usr/bin/python3
"""Command interpreter for the AirBnB clone."""

import ast
import cmd
import re
import shlex

from models import (
    Amenity,
    BaseModel,
    City,
    Place,
    Review,
    State,
    User,
    storage
)


class HBNBCommand(cmd.Cmd):
    """Provide commands for managing AirBnB objects."""

    prompt = "(hbnb) "

    classes = {
        "Amenity": Amenity,
        "BaseModel": BaseModel,
        "City": City,
        "Place": Place,
        "Review": Review,
        "State": State,
        "User": User
    }

    def emptyline(self):
        """Do nothing when an empty command is entered."""
        pass

    def do_quit(self, arg):
        """Quit command to exit the program."""
        return True

    def do_EOF(self, arg):
        """Exit the command interpreter using EOF."""
        print()
        return True

    def _class_from_name(self, class_name):
        """Return a supported class or print an error."""
        if not class_name:
            print("** class name missing **")
            return None

        model_class = self.classes.get(class_name)

        if model_class is None:
            print("** class doesn't exist **")
            return None

        return model_class

    def _object(self, class_name, object_id):
        """Return one stored object by class name and id."""
        model_class = self.classes[class_name]
        key = "{}.{}".format(class_name, object_id)

        return storage.all(model_class).get(key)

    def _create_parameters(self, text):
        """Parse create parameters into correctly typed values."""
        kwargs = {}

        pattern = re.compile(
            r'([A-Za-z_][A-Za-z0-9_]*)='
            r'("(?:\\.|[^"\\])*"|[^\s]+)'
        )

        for match in pattern.finditer(text):
            key = match.group(1)
            raw_value = match.group(2)

            if raw_value.startswith('"'):
                if not raw_value.endswith('"'):
                    continue

                value = raw_value[1:-1]
                value = value.replace('\\"', '"')
                value = value.replace("_", " ")

            else:
                try:
                    if "." in raw_value:
                        value = float(raw_value)
                    else:
                        value = int(raw_value)
                except ValueError:
                    continue

            kwargs[key] = value

        return kwargs

    def do_create(self, arg):
        """Create an object with optional key=value parameters."""
        if not arg.strip():
            print("** class name missing **")
            return

        parts = arg.strip().split(maxsplit=1)
        class_name = parts[0]

        model_class = self._class_from_name(class_name)

        if model_class is None:
            return

        parameter_text = ""

        if len(parts) > 1:
            parameter_text = parts[1]

        kwargs = self._create_parameters(parameter_text)

        obj = model_class(**kwargs)
        obj.save()

        print(obj.id)

    def do_show(self, arg):
        """Display an object by class and id."""
        args = shlex.split(arg)

        if not args:
            print("** class name missing **")
            return

        class_name = args[0]

        if self._class_from_name(class_name) is None:
            return

        if len(args) < 2:
            print("** instance id missing **")
            return

        obj = self._object(class_name, args[1])

        if obj is None:
            print("** no instance found **")
            return

        print(obj)

    def do_destroy(self, arg):
        """Delete an object by class and id."""
        args = shlex.split(arg)

        if not args:
            print("** class name missing **")
            return

        class_name = args[0]

        if self._class_from_name(class_name) is None:
            return

        if len(args) < 2:
            print("** instance id missing **")
            return

        obj = self._object(class_name, args[1])

        if obj is None:
            print("** no instance found **")
            return

        obj.delete()
        storage.save()

    def do_all(self, arg):
        """Display all objects, optionally filtered by class."""
        class_name = arg.strip()

        if class_name:
            model_class = self._class_from_name(class_name)

            if model_class is None:
                return

            objects = storage.all(model_class).values()
        else:
            objects = storage.all().values()

        print([str(obj) for obj in objects])

    def do_count(self, arg):
        """Print the number of objects belonging to a class."""
        class_name = arg.strip()

        model_class = self._class_from_name(class_name)

        if model_class is None:
            return

        print(len(storage.all(model_class)))

    def _convert_update_value(self, obj, name, value):
        """Convert a supplied update value to its model type."""
        if hasattr(obj, name):
            current = getattr(obj, name)

            if isinstance(current, bool):
                return value.lower() in ("true", "1")

            if isinstance(current, int):
                try:
                    return int(value)
                except ValueError:
                    return value

            if isinstance(current, float):
                try:
                    return float(value)
                except ValueError:
                    return value

        return value

    def do_update(self, arg):
        """Update one attribute of an existing object."""
        try:
            args = shlex.split(arg)
        except ValueError:
            args = arg.split()

        if not args:
            print("** class name missing **")
            return

        class_name = args[0]

        if self._class_from_name(class_name) is None:
            return

        if len(args) < 2:
            print("** instance id missing **")
            return

        obj = self._object(class_name, args[1])

        if obj is None:
            print("** no instance found **")
            return

        if len(args) < 3:
            print("** attribute name missing **")
            return

        if len(args) < 4:
            print("** value missing **")
            return

        name = args[2]
        value = self._convert_update_value(
            obj,
            name,
            args[3]
        )

        setattr(obj, name, value)
        obj.save()

    def default(self, line):
        """Handle <Class>.<command>() console notation."""
        match = re.fullmatch(
            r"([A-Za-z_][A-Za-z0-9_]*)\."
            r"(all|count|show|destroy|update)\((.*)\)",
            line.strip()
        )

        if match is None:
            return super().default(line)

        class_name = match.group(1)
        command = match.group(2)
        raw_args = match.group(3).strip()

        if class_name not in self.classes:
            print("** class doesn't exist **")
            return

        if command == "all":
            return self.do_all(class_name)

        if command == "count":
            return self.do_count(class_name)

        try:
            if raw_args:
                parsed = ast.literal_eval(
                    "(" + raw_args + ",)"
                )
            else:
                parsed = ()
        except (ValueError, SyntaxError):
            parsed = ()

        if command == "show":
            if not parsed:
                print("** instance id missing **")
                return

            return self.do_show(
                "{} {}".format(
                    class_name,
                    parsed[0]
                )
            )

        if command == "destroy":
            if not parsed:
                print("** instance id missing **")
                return

            return self.do_destroy(
                "{} {}".format(
                    class_name,
                    parsed[0]
                )
            )

        if command == "update":
            return self._dot_update(
                class_name,
                parsed
            )

    def _dot_update(self, class_name, args):
        """Handle dictionary and attribute dot-notation updates."""
        if not args:
            print("** instance id missing **")
            return

        obj = self._object(
            class_name,
            str(args[0])
        )

        if obj is None:
            print("** no instance found **")
            return

        if len(args) < 2:
            print("** attribute name missing **")
            return

        if isinstance(args[1], dict):
            for name, value in args[1].items():
                setattr(obj, name, value)

            obj.save()
            return

        if len(args) < 3:
            print("** value missing **")
            return

        setattr(
            obj,
            str(args[1]),
            args[2]
        )

        obj.save()


if __name__ == '__main__':
    HBNBCommand().cmdloop()
