from App.Objects.Mixins.Model import Model
from App.DB.DBInsertable import DBInsertable
from pydantic import Field, computed_field
from typing import Literal

class LinkData(Model, DBInsertable):
    role: list[Literal['object', 'thumbnail', 'common', 'external', 'revision', 'list_item', 'horizontal'] | str] = Field(default = ['object'])

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
