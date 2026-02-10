from App.Executables.Convertation import Convertation
from App.Responses.ObjectsList import ObjectsList
from Data.JSON import JSON
from Data.XML import XML
import xmltodict

class XMLToJson(Convertation):
    common_object = XML
    converts_to = JSON

    def implementation(self, i) -> ObjectsList:
        _item = JSON()
        _item.data = xmltodict.parse(i.get('orig').xml)

        return ObjectsList(items = [_item])
