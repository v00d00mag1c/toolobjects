from App.Objects.Object import Object
from pydantic import Field

class XML(Object):
    '''
    Using JSON to store XML string, huh?
    '''
    xml: str = Field()

    @classmethod
    def getConverters(cls) -> list:
        from Data.XMLToJson import XMLToJson

        return [XMLToJson]
