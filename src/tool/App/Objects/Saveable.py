from pydantic import Field
from datetime import datetime
from .ObjectMeta import ObjectMeta
from .Source import Source
from .SavedVia import SavedVia
from typing import ClassVar
from pydantic import Field, computed_field, field_serializer
from datetime import datetime

class Saveable():
    _internal_fields = ['collection', 'object_meta', 'saved_via']
    self_name: ClassVar[str] = 'Saveable'

    '''
    extend them as internal classes and annotate again when extending object
    '''
    source: Source = Field(default = Source())
    object_meta: ObjectMeta = Field(default = ObjectMeta())
    collection: bool = Field(default=False)

    @computed_field
    @property
    def saved_via(self) -> SavedVia:
        _item = SavedVia()
        _item.object_name = self.getClassNameJoined()

        if self.call != None and self.call._db != None:
            _item.call_id = self.call._db.uuid

        return _item

    created_at: datetime = Field(default_factory=lambda: datetime.now())
    declared_created_at: datetime = Field(default_factory=lambda: datetime.now())
    edited_at: datetime = Field(default=None)

    @field_serializer('created_at', 'declared_created_at', 'edited_at')
    def get_timestamp(self, dt: datetime, _info) -> int:
        if dt == None:
            return None

        return int(dt.timestamp())
