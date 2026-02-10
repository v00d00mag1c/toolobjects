from pydantic import Field
from datetime import datetime
from pydantic import BaseModel as PydanticBaseModel
from .Object import Object
from .Saved import Saved
from .Source import Source
from .ObjectMeta import ObjectMeta
from .Linkable import Linkable
from typing import ClassVar

class Saveable(Object, Linkable):
    '''
    Item that can be flushed into DB

    display_name: title that will be shown in the ui, is changeable
    original_name: title that was written after creation, meant to be unchangeable
    display_description: description that will 

    "unlisted" is probaly not needed here;
    '''

    self_name: ClassVar[str] = 'Saveable'

    display_name: str = Field(default=None)
    original_name: str = Field(default=None)
    display_description: str = Field(default=None)
    original_description: str = Field(default=None)
    index_description: str = Field(default=None)

    # Time of object creation
    created_at: datetime = Field(default_factory=lambda: datetime.now())
    edited_at: datetime = Field(default=None)

    # Time of object creation generally
    declared_created_at: datetime = Field(default_factory=lambda: datetime.now())

    '''
    If you want to extend these fields, extend them as internal classes and annotate again
    '''
    source: Source = Field(default = Source())
    object_meta: ObjectMeta = Field(default = ObjectMeta())
    saved: Saved = Field(default = Saved())

    collection: bool = Field(default=False)
    unlisted: bool = Field(default=False)

    def getContent(self):
        '''
        TODO: return all fields except those listed above
        '''
        pass
