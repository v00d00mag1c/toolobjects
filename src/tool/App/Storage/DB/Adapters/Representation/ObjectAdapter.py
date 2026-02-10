from Data.JSON import JSON
from App import app
from App.Objects.Relations.Link import Link as CommonLink
from typing import Any, Generator
from App.Objects.Object import Object
from abc import ABC, abstractmethod
from App.Storage.DB.Adapters.Representation.AbstractAdapter import AbstractAdapter
from App.Objects.Misc.UnknownObject import UnknownObject
import json

class ObjectAdapter(AbstractAdapter):
    content: str = None # Encoded json

    @abstractmethod
    def flush_content(self, item: Object):
        ...

    @abstractmethod
    def getLinks(self) -> Generator[CommonLink]:
        ...

    @abstractmethod
    def addLink(self, link: CommonLink):
        ...

    @abstractmethod
    def removeLink(self, link: CommonLink):
        ...

    def toPython(self):
        _object_name = None

        try:
            _content = JSON().fromText(self.content)
            _object_name = _content.data.get('obj').get('saved_via').get('object_name')
            _class = app.ObjectsList.getByName(_object_name).getModule()
            _item = _class.model_validate(_content.data, strict = False)
            _item.setDb(self)

            return _item
        except (AttributeError, json.decoder.JSONDecodeError) as e:
            _msg = f"Object with uuid {self.uuid} was tried to be loaded, "

            if _object_name == None:
                _msg += f"obj.saved_via.object_name is not accesible"
            else:
                _msg += f"type is {_object_name}, {str(e)}"

            _msg += ". UnknownObject returned"

            app.Logger.log(message = _msg, role = ["object_adapter_db_import"])

            return UnknownObject()
