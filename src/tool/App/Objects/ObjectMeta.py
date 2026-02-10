from pydantic import BaseModel, Field, field_serializer
from datetime import datetime

class ObjectMeta(BaseModel):
    '''
    Additional data about object
    '''
    name: str = Field(default=None)
    description: str = Field(default=None)
    indexation: str = Field(default=None)
    original_name: str = Field(default=None)
    original_description: str = Field(default=None)
    thumbnail: dict = Field(default = None)
    duration: int = Field(default = None)
    role: list[str] = Field(default = None) # dont know yet where to use
    object_names: list[str] = Field(default = None) # Custom saved_via.object_names
    collection: bool = Field(default=False) # Is a collection

    created_at: datetime = Field(default_factory=lambda: datetime.now())
    declared_created_at: datetime = Field(default_factory=lambda: datetime.now())
    edited_at: datetime = Field(default=None)

    @field_serializer('created_at', 'declared_created_at', 'edited_at')
    def get_timestamp(self, dt: datetime, _info) -> int:
        if dt == None:
            return None

        return int(dt.timestamp())
