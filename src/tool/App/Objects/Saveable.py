from .ObjectMeta import ObjectMeta
from .SavedVia import SavedVia
from typing import ClassVar
from pydantic import Field, computed_field

class Saveable():
    self_name: ClassVar[str] = 'Saveable'

    '''
    extend them as internal classes and annotate again when extending object
    '''

    @computed_field(repr = False)
    @property
    def obj(self) -> ObjectMeta:
        _item = ObjectMeta()
        _item.saved_via = SavedVia()
        _item.saved_via.object_name = self.getClassNameJoined()

        '''
        if self.call != None and self.call._db != None:
            _item.call_id = self.call._db.uuid
        '''
        return _item
