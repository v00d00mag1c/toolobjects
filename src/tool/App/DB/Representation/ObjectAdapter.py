from Data.Types.JSON import JSON
from App import app
from App.Objects.Relations.Link import Link as CommonLink
from typing import Any, Generator
from App.Objects.Object import Object
from abc import ABC, abstractmethod
from App.DB.Representation.AbstractAdapter import AbstractAdapter
from App.Objects.Misc.Migrated import Migrated
import json
from pydantic import ValidationError

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

    @abstractmethod
    def deleteFromDB(self, remove_links: bool = True):
        ...

    def _parseJson(self) -> dict:
        return JSON().fromText(self.content).data

    def get_permission_to_flush(self, item: Object):
        _storage = self._adapter._storage_item
        if _storage.allowed_objects != None:
            assert item.mro_name_check(_storage.allowed_objects) == True, 'object is not allowed to flush'

        if _storage.forbidden_objects != None:
            assert item.mro_name_check(_storage.forbidden_objects) == False, 'object with this type is forbidden in this db'

        return True

    def toPython(self):
        _object_name = None
        _content = None

        try:
            _content = self._parseJson()
            _object_name = _content.get('obj').get('saved_via').get('object_name')
            _class = app.ObjectsList.getByName(_object_name).getModule()

            # If found that class is migrated, use class that it references. also there is content passed, it may be used to check types of schema idk
            if _class.isInMRO(Migrated):
                _class = _class.get_migrated_to(_content)

            _item = _class.model_validate(_content, strict = False)
            _item.setDb(self)

            return _item
        except (AttributeError, json.decoder.JSONDecodeError, ValidationError) as e:
            _msg = f"Object with uuid {self.uuid} was tried to be loaded, "
            _msg2 = ''

            if _object_name == None:
                _msg2 = f"obj.saved_via.object_name is not accesible"
            else:
                _msg2 = f"type is {_object_name}, {str(e)}"

            _msg += _msg2 + ". UnknownObject returned"

            app.Logger.log(message = _msg, role = ['error', 'storage.adapter.db.import'])

            return self.toUnknown(reason = _msg2, content = _content)
        except Exception as e:
            app.Logger.log(e, role = ['error'])

            return self.toUnknown(reason = str(e))
