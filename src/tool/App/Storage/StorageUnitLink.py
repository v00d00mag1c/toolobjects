from App.Objects.Mixins.Model import Model
from App.Objects.Relations.LinkInsertion import LinkInsertion
from App.DB.DBInsertable import DBInsertable
from App.Objects.Mixins.Section import Section
from pydantic import Field, model_serializer

class StorageUnitLink(Model, DBInsertable, Section):
    path: str = Field()
    insertion: LinkInsertion = Field()

    def get_storage_unit(self):
        return self._get('insertion')
