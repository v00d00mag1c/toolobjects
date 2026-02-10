from pydantic import BaseModel, Field, model_serializer
from typing import Any
from App.Storage.DB.DBInsertable import DBInsertable
from App.Objects.Mixins.Section import Section

class LinkInsertion(BaseModel, DBInsertable, Section):
    link: int | Any = Field()
    field: list[str] = Field(default = [])
    #additional: dict = Field(default = {})

    def _getLink(self):
        if type(self.link) == int:
            _lnk = self.getDb()._adapter.LinkAdapter.getById(self.link)
            if _lnk == None:
                return None

            return _lnk.toPython()

        return self.link

    def unwrap(self):
        _item = getattr(self._getLink(), 'item')

        if len(self.field) > 0:
            _main_item = _item
            for link in self.field:
                _main_item = getattr(_main_item, link, None)

            return _main_item

        return _item

    @model_serializer
    def serialize(self) -> dict:
        vals = dict()
        vals['field'] = self.field
        _lnk = self._getLink()
        if _lnk != None and _lnk.getDb() != None:
            vals['link'] = self._getLink().getDbId()

        return vals
