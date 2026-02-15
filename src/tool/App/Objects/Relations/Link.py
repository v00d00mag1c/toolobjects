from App.Objects.Mixins.Model import Model
from App.DB.DBInsertable import DBInsertable
from App.Objects.Relations.LinkInsertion import LinkInsertion
from App.Objects.Relations.LinkData import LinkData
from pydantic import Field, computed_field
from typing import Any

class Link(Model, DBInsertable):
    item: Any = Field()
    data: LinkData = Field(default = LinkData())

    def toInsert(self, field: list[str] = []) -> LinkInsertion:
        return LinkInsertion(
            link = self,
            field = field
        )

    def getItem(self):
        return self.item
