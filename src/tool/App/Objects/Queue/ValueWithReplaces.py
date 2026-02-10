from App.Objects.Object import Object
from pydantic import Field
from App.Objects.Queue.LinkValue import LinkValue

class Replacement(Object):
    position: list[int] = Field(default = None)
    value: str = Field(default = None)

class ValueWithReplaces(Object):
    replacements: list[Replacement] = None
    value: str = None

    def toString(self, prestart: dict, items: list):
        _ret = self.value

        for item in self.replacements:
            _ret = '{0}{1}{2}'.format(_ret[:item.position[0]], LinkValue(value = item.value).toString(prestart, items), _ret[item.position[1]:])

        return _ret
