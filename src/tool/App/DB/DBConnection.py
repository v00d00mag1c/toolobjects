from App.Objects.Object import Object
from pydantic import Field
from typing import Literal

class DBConnection(Object):
    '''
    Object that describes available db types
    '''

    protocol: Literal['sqlite'] = Field()
    content: str | dict = Field(default = None)
