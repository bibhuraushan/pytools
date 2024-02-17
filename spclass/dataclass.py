from typing import Any


class DictAttr(dict):
    # """ 
    # A python class to make dictionary element accesible by attribute.
    # """

    def __getattr__(self, name: str) -> Any:
        """
        Special Function to get value of given key.

        Parameters
        ----------
        name : str
            Key name.

        Returns
        -------
        Any
            Return value from Dictionary.
        """
        return self.get(name)
    
    def __setattr__(self, name: str, value: Any) -> None:
        """
        To set or update attribute to dictionary

        Parameters
        ----------
        name : str
            Name of the key
        value : Any
            Value to be added or updated
        """

        self[name] = value

    def __repr__(self) -> str:
        """

        Returns
        -------
        str
           Foramted repr().
        """
        classname = self.__class__.__name__
        _temp = dict(zip(self.keys(), self.values()))
        return f"{classname}({_temp})"
    
    def __str__(self) -> str:
        """
        String formater.

        Returns
        -------
        str
            Formated string output.
        """
        _temp = ''
        for _key in self.keys():
            _temp += f"{_key:>10s}: {self.get(_key)}\n"
        return _temp

    @property
    def dictionary(self):
        """
        Returns dictionary.

        Returns
        -------
        dictionary: dict
            Returns dictionary.
        """
        return self