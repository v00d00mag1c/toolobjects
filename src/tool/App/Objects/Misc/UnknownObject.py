from App.Objects.Object import Object
from pydantic import Field

class UnknownObject(Object):
    '''
    returns if object with specified name was not found
    '''

    reason: str = Field(default = None)
