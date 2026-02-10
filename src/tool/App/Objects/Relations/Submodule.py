from App.Objects.Mixins.Model import Model
from typing import Literal
from pydantic import Field, field_serializer
from App.Objects.Index.ModuleData import ModuleData
from typing import Any

class Submodule(Model):
    '''
    Submodule of an object

    roles:

    usage: This object is used in _implementation() and the all arguments should take from this too

    object: Object class related to current Object

    wheel: used by App.Executables.Wheel

    convertation: will be used for convertTo
    '''

    item: Any = Field()
    role: list[Literal['link_allowed', 'usage', 'action', 'object_in', 'object_out', 'object', 'thumbnail', 'thumbnail_disabled_default', 'common', 'wheel', 'convertation', 'test', 'returns', 'allowed_view'] | str] = Field(default = ['common'])

    @field_serializer('item')
    def get_item(self, item) -> str:
        if item == None:
            return None

        return ModuleData.from_module(item)
