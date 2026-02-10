from App.Objects.BaseModel import BaseModel
from pydantic import Field
from typing import Any, Literal
from enum import Enum

class Submodule(BaseModel):
    '''
    Link to another module
    '''

    class ConnectionEnum(Enum):
        INTERNAL = 0
        EXTERNAL = 1 # function

    module: Any
    value: ConnectionEnum = Field(default = ConnectionEnum.INTERNAL.value)
    role: list[Literal['object', 'wheel']] = Field(default = ['object'])
    '''
    what roles are exists?
    
    object - part of common objec
    wheel - will be used in Client or Wheel
    '''
