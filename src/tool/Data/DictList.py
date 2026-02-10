from typing import Any, Generator
from App.Objects.Object import Object
from App.Objects.Misc.NameContainable import NameContainable
from pydantic import BaseModel, Field

class DictList(Object):
    '''
    List with object that contains "name" field and so can be used as Dict
    '''

    items: list[NameContainable] = Field(default = []) # name-field-containing

    def toList(self) -> list:
        return self.items

    def iterate(self) -> Generator:
        for item in self.toList():
            yield item

    def toNames(self) -> list:
        names = []
        for val in self.toList():
            names.append(val.get_name_for_dictlist())

        return names

    def toDict(self) -> dict:
        dicts = {}
        for item in self.items:
            dicts[item.get_name_for_dictlist()] = item

        return dicts

    def get(self, name: str) -> Any:
        for item in self.toList():
            if item.is_name_equals(name):
                return item

    def append(self, item: Any):
        self.items.append(item)
