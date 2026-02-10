from App.Objects.Mixins.BaseModel import BaseModel
from App.Objects.Misc.LinkInsertion import LinkInsertion
from App.Storage.DB.DBInsertable import DBInsertable
from App.Objects.Mixins.Section import Section
from pydantic import Field, model_serializer

class StorageUnitLink(BaseModel, DBInsertable, Section):
    path: str = Field()
    insertion: LinkInsertion = Field()
