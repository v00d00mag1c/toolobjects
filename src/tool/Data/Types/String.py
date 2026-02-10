from App.Objects.Object import Object
from pydantic import Field
from App.Objects.Act import Act

class String(Object):
    value: str = Field()

    @classmethod
    def asArgument(cls, val):
        if val == None:
            return None

        return str(val)

    @staticmethod
    def cut(string: str, length: int = 100, short_str: str = '...'):
        if len(string) >= length - len(short_str):
            return string[0:length] + short_str

        return string

    def _display_as_string(self):
        return str(self.value)
