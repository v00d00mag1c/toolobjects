from App.Responses.Response import Response
from App.Objects.Object import Object
from App.Objects.Submodule import Submodule
from pydantic import Field

class ObjectsList(Response):
    items: list[Object] = Field(default = [])

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
