from ..Argument import Argument
from typing import Any
from pydantic import Field, computed_field

class Orig(Argument):
    '''
    Converts JSON into pydantic model
    '''
    orig: Any = Field(default = None)

    def implementation(self, original_value: str):
        if self.orig == None:
            return original_value
        
        if isinstance(original_value, self.object):
            return original_value

        _item = self.object
        _item.model_validate(original_value)

        return _item(**original_value)
