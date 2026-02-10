from App.Objects.Object import Object
from pydantic import Field
from App.Objects.Submodule import Submodule

class XML(Object):
    # Using JSON to store XML string, huh?

    xml: str = Field()

    @classmethod
    def getSubmodules(cls) -> list:
        from Data.XMLToJson import XMLToJson

        return [
            Submodule(
                module = XMLToJson,
                role = ['convertation']
            )
        ]
