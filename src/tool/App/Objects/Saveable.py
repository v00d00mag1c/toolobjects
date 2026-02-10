from pydantic import Field
from datetime import datetime
from pydantic import BaseModel as PydanticBaseModel, computed_field
from .Object import Object
from .SavedVia import SavedVia
from .Source import Source
from .ObjectMeta import ObjectMeta
from .Linkable import Linkable
from .AllowExtraFields import AllowExtraFields
from typing import ClassVar

class Saveable(Object, Linkable, AllowExtraFields):
    '''
    Item that can be flushed into DB

    display_name: title that will be shown in the ui, is changeable
    original_name: title that was written after creation, meant to be unchangeable
    display_description: description that will 

    "unlisted" is probaly not needed here;
    '''

    self_name: ClassVar[str] = 'Saveable'

    # set by implementation
    original_name: str = Field(default=None)
    original_description: str = Field(default=None)
    created_at: datetime = Field(default_factory=lambda: datetime.now())
    declared_created_at: datetime = Field(default_factory=lambda: datetime.now())

    '''
    extend them as internal classes and annotate again if you want to extend
    '''
    source: Source = Field(default = Source())
    object_meta: ObjectMeta = Field(default = ObjectMeta())

    @computed_field
    @property
    def saved_via(self) -> SavedVia:
        _item = SavedVia()
        _item.object_name = self.getClassNameJoined()

        if self.call != None and self.call._db != None:
            _item.call_id = self.call._db.uuid

        return _item

    # set by user
    display_name: str = Field(default=None)
    display_description: str = Field(default=None)
    index_description: str = Field(default=None)
    edited_at: datetime = Field(default=None)

    # types
    collection: bool = Field(default=False)
    unlisted: bool = Field(default=False)

    def getContent(self):
        '''
        TODO: return all fields except those listed above
        '''
        pass
