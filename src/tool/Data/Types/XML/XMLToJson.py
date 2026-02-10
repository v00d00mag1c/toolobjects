from App.Objects.Convertation import Convertation
from App.Objects.Responses.ObjectsList import ObjectsList
from App.Objects.Relations.Submodule import Submodule
from App.Objects.Requirements.Requirement import Requirement
from Data.Types.JSON import JSON
from Data.Types.XML.XML import XML

class XMLToJson(Convertation):
    def _implementation(self, i) -> ObjectsList:
        import xmltodict

        _item = JSON()
        _item.data = xmltodict.parse(i.get('orig').xml)

        return ObjectsList(items = [_item])

    @classmethod
    def _requirements(cls):
        return [
            Requirement(
                name = 'xmltodict'
            )
        ]

    @classmethod
    def _submodules(cls) -> list[Submodule]:
        return [
            Submodule(
                item = XML,
                role = ['object_in']
            ),
            Submodule(
                item = JSON,
                role = ['object_out']
            )
        ]
