from App.Objects.Object import Object
from pydantic import Field
from App.Objects.Relations.Submodule import Submodule

class XML(Object):
    # Using JSON to store XML string, huh?

    xml: str = Field()

    @classmethod
    def _submodules(cls) -> list:
        from Data.Types.XML.XMLToJson import XMLToJson

        return [
            Submodule(
                item = XMLToJson,
                role = ['convertation']
            )
        ]
