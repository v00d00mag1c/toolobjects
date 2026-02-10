from pydantic import Field, field_serializer
from App.Objects.Mixins.BaseModel import BaseModel
from datetime import datetime
from typing import Optional
from .Source import Source
from .SavedVia import SavedVia

class ObjectMeta(BaseModel):
    '''
    Additional data about object
    '''

    saved_via: SavedVia = Field(default = None)
    name: Optional[str] = Field(default=None)
    description: Optional[str] = Field(default=None)
    indexation: Optional[str] = Field(default=None)
    original_name: Optional[str] = Field(default=None)
    original_description: Optional[str] = Field(default=None)
    thumbnail: Optional[dict] = Field(default = None)
    duration: Optional[int] = Field(default = None)
    role: Optional[list[str]] = Field(default = None) # dont know yet where to use
    object_names: Optional[list[str]] = Field(default = None) # Custom saved_via.object_names
    collection: Optional[bool] = Field(default=False) # Is a collection
    source: Source = Field(default = Source(), repr = False)

    created_at: Optional[datetime] = Field(default_factory=lambda: datetime.now())
    declared_created_at: Optional[datetime] = Field(default_factory=lambda: datetime.now())
    edited_at: Optional[datetime] = Field(default=None)
