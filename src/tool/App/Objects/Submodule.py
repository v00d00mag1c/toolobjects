from App.Objects.BaseModel import BaseModel
from pydantic import Field
from typing import Any, Literal
from enum import Enum

class SubmoduleConnectionTypeEnum(Enum):
    INTERNAL = 0
    EXTERNAL = 1 # function

class Submodule(BaseModel):
    '''
    Link to another module
    '''

    module: Any
    value: SubmoduleConnectionTypeEnum = Field(default = SubmoduleConnectionTypeEnum.INTERNAL.value)
