"""
This module provides utility classes for handling and manipulating dictionaries in Python.

Classes
-------
DictAttr : dict
    A subclass of `dict` that allows attribute-style access to dictionary keys.
DictConvertor
    A utility class for converting dictionaries to various formats (e.g., JSON, YAML) and 
    creating `DictAttr` objects for attribute-style access.

Examples
--------
Basic usage of `DictAttr`:

>>> my_dict = DictAttr({"key1": "value1", "key2": "value2"})
>>> print(my_dict.key1)  # Accessing dictionary values as attributes
value1
>>> my_dict.key3 = "value3"  # Adding a new key-value pair
>>> print(my_dict)
       key1: value1
       key2: value2
       key3: value3

Using `DictConvertor` to save dictionaries as JSON/YAML:

>>> converter = DictConvertor({"name": "John", "age": 30})
>>> converter.to_json("output.json")  # Saves dictionary as a JSON file
>>> converter.to_yaml("output.yaml")  # Saves dictionary as a YAML file

Converting dictionaries to `DictAttr` objects:

>>> for obj in converter.to_object():
>>>     print(obj.name, obj.age)
John 30
"""

from typing import Any, Generator
import json
import yaml


class DictAttr(dict):
    """
    A Python class to make dictionary elements accessible as attributes.

    This class inherits from `dict` and allows attribute-style access to dictionary keys.
    """

    def __getattr__(self, name: str) -> Any:
        """
        Retrieve the value of the specified key using attribute-style access.

        Parameters
        ----------
        name : str
            The key name to retrieve.

        Returns
        -------
        Any
            The value associated with the specified key, or None if the key does not exist.
        """
        return self.get(name)

    def __setattr__(self, name: str, value: Any) -> None:
        """
        Set or update a key-value pair using attribute-style assignment.

        Parameters
        ----------
        name : str
            The key name to set or update.
        value : Any
            The value to assign to the specified key.
        """
        self[name] = value

    def __repr__(self) -> str:
        """
        Provide a formatted string representation of the object.

        Returns
        -------
        str
            A string representation of the object.
        """
        classname = self.__class__.__name__
        _temp = dict(zip(self.keys(), self.values()))
        return f"{classname}({_temp})"

    def __str__(self) -> str:
        """
        Provide a formatted string for printing the dictionary contents.

        Returns
        -------
        str
            A formatted string representing the dictionary.
        """
        _temp = ""
        for _key in self.keys():
            _temp += f"{_key:>10s}: {self.get(_key)}\n"
        return _temp

    @property
    def dictionary(self) -> dict:
        """
        Retrieve the dictionary representation of the object.

        Returns
        -------
        dict
            The dictionary stored in the object.
        """
        return self


class DictConvertor:
    """
    A utility class to handle conversions of a dictionary to various formats.

    This class provides methods to save dictionaries as JSON or YAML files and
    convert them into `DictAttr` objects for attribute-style access.
    """

    def __init__(self, dictionary: dict):
        """
        Initialize the `DictConvertor` with a dictionary.

        Parameters
        ----------
        dictionary : dict
            The input dictionary to be processed.
        """
        if len(dictionary) == 1:
            self.dictionary = [dictionary]
        else:
            self.dictionary = dictionary

    def to_json(self, filename: str) -> None:
        """
        Save the dictionary as a JSON file.

        Parameters
        ----------
        filename : str
            The name of the file to save the JSON content.
        """
        with open(filename, "w") as file:
            json.dump(self.dictionary, file, indent=4)

    def to_yaml(self, filename: str) -> None:
        """
        Save the dictionary as a YAML file.

        Parameters
        ----------
        filename : str
            The name of the file to save the YAML content.
        """
        with open(filename, "w") as file:
            yaml.dump(self.dictionary, file)

    def to_object(self) -> Generator[DictAttr, None, None]:
        """
        Convert the dictionary into `DictAttr` objects for attribute-style access.

        Yields
        ------
        DictAttr
            An instance of `DictAttr` for each dictionary in the input.
        """
        for _dict in self.dictionary:
            yield DictAttr(_dict)
