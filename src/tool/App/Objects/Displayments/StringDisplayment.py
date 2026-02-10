from App.Objects.Displayments.Displayment import Displayment
from pydantic import Field
from typing import Any, ClassVar

class StringDisplayment(Displayment):
    '''
    Class that display object some way
    '''

    display_type: ClassVar[str] = 'any'
    role: list[str] = Field(default = [])

    value: str | Any = None # probaly module

    def implementation(self, i: dict) -> Any:
        '''
        The object to display is passed in i.get("object")
        '''

        orig = i.get('orig')

        return '0'
