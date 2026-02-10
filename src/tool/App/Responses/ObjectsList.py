from App.Responses.Response import Response
from App.Objects.Object import Object
from App.Objects.Relations.Submodule import Submodule
from pydantic import Field
from typing import Generator

class ObjectsList(Response):
    '''
    The best Response type
    '''

    items: list[Object] = Field(default = [])
    supposed_to_be_single: bool = Field(default = False)

    def append(self, item: Object):
        self.items.append(item)

    def first(self):
        return self.items[0]

    def getCount(self) -> int:
        return len(self.items)

    def getItems(self) -> Generator[Object]:
        for item in self.items:
            yield item

    def getPrevailingObjects(self) -> list[dict]:
        '''
        Returns dictionaries:

        "object": Link to class
        "count": Count of object with this class
        '''
        pass

    def getAvailableConvertations(self) -> list[Submodule]:
        pass

    def imagineAs(self) -> list[Object]:
        '''
        calls "convertTo()" to every item
        '''
        pass

    @staticmethod
    def fromItems(items):
        new = ObjectsList(items = items)

        return new
