from App.Objects.Relations.Link import Link
from typing import Literal
from pydantic import Field

class Submodule(Link):
    '''
    Submodule of an object

    roles:

    object: Object class related to current Object

    wheel: used by App.Executables.Wheel

    convertation: will be used for convertTo
    '''

    role: list[Literal['action', 'object_in', 'object_out', 'object', 'thumbnail', 'common', 'wheel', 'convertation', 'test'] | str] = Field(default = ['common'])
