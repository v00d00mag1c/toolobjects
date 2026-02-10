from typing import Any, Generator
from App.Objects.Object import Object
from pydantic import BaseModel

class DictList(Object):
    '''
    List with object that contains "name" field and so can be used as Dict
    '''

    items: list[Object] # name-field-containing

    def toList(self) -> list:
        return self.items

    def iterate(self) -> Generator:
        for item in self.toList():
            yield item

    def toNames(self) -> list:
        names = []
        for val in self.toList():
            names.append(val.name)

        return names

    def toDict(self) -> dict:
        dicts = {}
        for item in self.items:
            dicts[item.name] = item

        return dicts

    def get(self, name: str) -> Any:
        for item in self.toList():
            if item.name == name:
                return item

    def append(self, item: Any):
        self.items.append(item)
