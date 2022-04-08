"""
Brocoli module. 🥦
"""

import os
import json
from io import TextIOWrapper

class BrocoliError(BaseException): pass # base error


class BaseBrocoli(object):

    # === Utilities === #

    def __init__(self, path: str, _create = False) -> None:
        """
        Base class for all Brocolis instances.
        """
        
        # loading
        self.path = path
        try: self.file = open(path, 'w+' if _create else 'r+')
        except Exception as e: raise BrocoliError('Could not open file. Reveived error: {e}')

        # decoding
        try: self.base = json.loads(self.file.read())
        except Exception as e: raise BrocoliError(f'Could not decode the JSON. Received error: {e}')

    def __str__(self) -> str: return str(self.base)

    def submit(self) -> None:
        """
        Overwrite the file after the modifications.
        """

        self.file.write(json.dumps(self.base))

    # === Base functions === #

    def delete(self):
        """
        Delete the file.
        """
        
        try: os.remove(self.path)
        except Exception as e: raise BrocoliError(f'Could not delete file. Received error: {e}')

    def getDict(self):
        """
        Return the content of the file formatted as a python dictionnary object.
        """

        return self.base

    # === Read functions === #

    def get(self, prop) -> str:
        """
        Gets a property.
        """

        try: return self.base[prop]
        except KeyError: raise BrocoliError('This property does not exists!')

    # === Write functions === # 

    def add(self, prop: str, value: str) -> None:
        """
        Adds a property to the base.
        """

        if prop in self.base.keys(): raise BrocoliError('This key already exists!')

        self.base[prop] = value
    
    def pop(self, prop) -> str:
        """
        Removes a property of the base and returns it.
        """

        return self.base.pop(prop)

    def set(self, prop, value) -> str:
        """
        Overwrite the value of a property.
        """

        self.add(prop, value)


class New(BaseBrocoli):
    def __init__(self, name:str) -> None:
        """
        Creates a new Brocoli instance with a new file.
        """
        
        super().__init__(str(name), _create = True)


class Open(BaseBrocoli):
    def __init__(self, path: str) -> None:
        """
        Creates a instance of Brocoli using the path of an alreay created file.
        """

        super().__init__(str(path))

# TODO: fix New
# TODO: fix erasing when openning