from App.Objects.Mixins.BaseModel import BaseModel
from pydantic import Field
from typing import ClassVar

class Displayment(BaseModel):
    '''
    Class that display object some way
    '''

    display_type: ClassVar[str] = 'any'
    role: list[str] = Field(default = [])
