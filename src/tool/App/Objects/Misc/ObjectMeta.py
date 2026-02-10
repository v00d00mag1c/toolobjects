from pydantic import Field, field_serializer
from App.Objects.Mixins.BaseModel import BaseModel
from datetime import datetime
from typing import Optional
from .Source import Source
from .Thumbnail import Thumbnail
from .SavedVia import SavedVia

class ObjectMeta(BaseModel):
    saved_via: SavedVia = Field(default = None)
    custom_saved_via: Optional[list[SavedVia]] = Field(default = [])

    name: Optional[str] = Field(default=None)
    original_name: Optional[str] = Field(default=None)

    description: Optional[str] = Field(default=None)
    shadow_description: Optional[str] = Field(default=None)
    original_description: Optional[str] = Field(default=None)

    role: Optional[list[str]] = Field(default = [])
    duration: Optional[int] = Field(default = None)

    collection: Optional[bool] = Field(default=False)
    public: Optional[bool] = Field(default=False)

    source: list[Source] = Field(default = [], repr = False)
    thumbnail: Optional[list[Thumbnail]] = Field(default = [])

    created_at: Optional[datetime] = Field(default_factory=lambda: datetime.now())
    edited_at: Optional[datetime] = Field(default=None)
    declared_created_at: Optional[datetime] = Field(default_factory=lambda: datetime.now())

    @property
    def any_name(self):
        if self.name == None:
            return self.original_name

        return self.name

    def set_common_source(self, source: Source):
        source.is_common = True

        self.source.append(source)

    def add_source(self, source: Source):
        self.source.append(source)

    def add_thumbnail(self, thumb: Thumbnail):
        self.thumbnail.append(thumb)

    def make_public(self):
        self.public = True

    def get_common_source(self):
        for source in self.source:
            if source.is_common == True:
                return source
