from App.Objects.BaseModel import BaseModel, computed_field
from App.Storage.DB.DBInsertable import DBInsertable
from App.Objects.LinkInsertion import LinkInsertion
from pydantic import Field
from typing import Any, Literal
from enum import Enum

class Link(BaseModel, DBInsertable):
    '''
    Link to an object.

    role is describes Link's relation to Object or its content

    object: related to internal content of Object
    thumbnail: related to Object's preview
    common: is common to object (storage unit or something)
    revision: another version of current object
    '''

    item: Any = Field() # : Object
    role: list[Literal['object', 'thumbnail', 'common', 'revision'] | str] = Field(default = ['object'])

    @computed_field
    @property
    def is_common(self) -> bool:
        return 'common' in self.role

    @computed_field
    @property
    def is_internal(self) -> bool:
        return 'external' not in self.role

    @computed_field
    @property
    def is_external(self) -> bool:
        return 'external' in self.role

    def toInsert(self, field: list[str] = []) -> LinkInsertion:
        return LinkInsertion(
            link = self,
            field = field
        )
