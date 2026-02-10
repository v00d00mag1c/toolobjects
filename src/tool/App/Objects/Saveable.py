from pydantic import Field
from .ObjectMeta import ObjectMeta
from .Source import Source
from .SavedVia import SavedVia
from typing import ClassVar
from pydantic import Field, computed_field

class Saveable():
    _internal_fields = ['collection', 'object_meta', 'saved_via']
    self_name: ClassVar[str] = 'Saveable'

    '''
    extend them as internal classes and annotate again when extending object
    '''
    source: Source = Field(default = Source(), repr = False)
    meta: ObjectMeta = Field(default = ObjectMeta(), repr = False)

    @computed_field
    @property
    def saved_via(self) -> SavedVia:
        _item = SavedVia()
        _item.object_name = self.getClassNameJoined()

        '''
        if self.call != None and self.call._db != None:
            _item.call_id = self.call._db.uuid
        '''
        return _item
