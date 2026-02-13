from pydantic import Field, field_serializer
from datetime import datetime
from typing import Optional
from App.Objects.Mixins.Model import Model
from App.Objects.Misc.Source import Source
from App.Objects.Misc.SavedVia import SavedVia
from App.Objects.Misc.Geo import Geo

class ObjectMeta(Model):
    saved_via: SavedVia = Field(default = None)

    name: Optional[str] = Field(default=None)
    description: Optional[str] = Field(default=None)

    collection: Optional[bool] = Field(default=False)
    role: Optional[list[str]] = Field(default = [])

    source: list[Source] = Field(default = [], repr = False)

    created_at: Optional[datetime] = Field(default=None)
    updated_at: Optional[datetime] = Field(default=None)

    # other fields
    geo: Optional[list[Geo]] = Field(default = None)
    width: Optional[float] = Field(default = None)
    height: Optional[float] = Field(default = None)
    duration: Optional[float] = Field(default = None)

    # other 2
    is_tmp: Optional[bool] = Field(default = False)
    is_internal: Optional[bool] = Field(default = False)
    is_forced: Optional[bool] = Field(default = False)

    def set_common_source(self, source: Source):
        source.is_common = True

        self.source.append(source)

    def add_source(self, source: Source):
        self.source.append(source)

    def get_common_source(self):
        for source in self.source:
            if source.is_common == True:
                return source

    def has_dimensions(self) -> bool:
        return self.width != None

    def set_tmp(self):
        self.is_tmp = True
