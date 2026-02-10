from App.Objects.Misc.Valueable import Valueable
from App.Objects.Act import Act
from pydantic import Field
from typing import Optional

class String(Valueable):
    value: Optional[str] = Field(default = None)
    min_length: Optional[int] = Field(default = None)
    max_length: Optional[int] = Field(default = None)

    @classmethod
    def asArgument(cls, val):
        if val == None:
            return None

        return str(val)

    def asArgumentAsInstance(self, val):
        if val == None:
            return None

        if self.min_length != None:
            assert len(val) > self.min_length, 'string is too short'

        if self.max_length != None:
            assert len(val) < self.max_length, 'string is too long'

        return str(val)

    @staticmethod
    def cut(string: str, length: int = 100, short_str: str = '...'):
        if len(string) >= length - len(short_str):
            return string[0:length] + short_str

        return string

    def _display_as_string(self):
        return str(self.value)
