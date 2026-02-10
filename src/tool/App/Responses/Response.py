from App.Objects.Object import Object
from typing import Any

class Response(Object):
    '''
    Object for wrapping responses from Executable. Must be extended with unique field

    class fields must not be used directly
    '''

    def toData(self) -> Any:
        pass

    @staticmethod
    def fromItems(items):
        '''
        Allows to create Response without constructor
        '''
        pass
