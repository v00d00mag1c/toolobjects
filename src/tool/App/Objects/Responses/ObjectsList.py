from App.Objects.Responses.Response import Response
from App.Objects.Object import Object
from App.Objects.Relations.Submodule import Submodule
from pydantic import Field
from typing import Generator
from App.Storage.StorageUUID import StorageUUID

class ObjectsList(Response):
    '''
    The best Response type
    '''

    items: list[Object] = Field(default = [])
    total_count: int = Field(default = 0)
    supposed_to_be_single: bool = Field(default = False)
    unsaveable: bool = Field(default = True)
    # If your Executable returns something that should be saved, "unsaveable" should be False. But if it searches something, it should be True because it will be re-flushed in DefaultExtractorWheel

    def append(self, item: Object):
        self.items.append(item)

    def first(self):
        return self.items[0]

    def getCount(self) -> int:
        return len(self.items)

    def getItems(self) -> Generator[Object]:
        for item in self.items:
            yield item

    @classmethod
    def asArgument(cls, val: str) -> Object:
        if type(val) == list:
            _obj = cls()
            for item in val:
                _item = StorageUUID.fromString(item)
                _obj.append(_item.toPython())

            return _obj

        return super().asArgument(val)

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

    def join(self, objects_list: Response):
        for item in objects_list.getItems():
            self.append(item)

    def should_be_saved(self) -> bool:
        return self.unsaveable == False
