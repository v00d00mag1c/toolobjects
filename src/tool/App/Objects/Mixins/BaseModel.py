from pydantic import BaseModel as PydanticBaseModel
from typing import Any
from App.Objects.Misc.ObjectMeta import ObjectMeta
from App.Objects.Misc.SavedVia import SavedVia
from App.Objects.Mixins.Model import Model
from pydantic import Field, model_validator

class BaseModel(Model):
    obj: ObjectMeta = Field(default = ObjectMeta())

    @model_validator(mode='after')
    def _saved_via(self):
        self.obj.saved_via = SavedVia()
        self.obj.saved_via.object_name = self.getClassNameJoined()

        return self

    @classmethod
    def asClass(cls, val: Any):
        if isinstance(val, cls):
            return val

        if val == None:
            return None

        return cls.model_validate(val)

    @classmethod
    def asArgument(cls, val: Any):
        return cls.asClass(val)

    @classmethod
    def mount(cls):
        '''
        Method that called after loading
        '''
        pass

    def _get(self, field, default = None):
        # If field is link insertion, unwrapping it and getting as normal value

        _field = getattr(self, field, default)
        if hasattr(_field, '_link_insertion_type') == True:
            return _field.unwrap()

        return _field

    def _set(self, field, value = None):
        setattr(self, field, value)

    @classmethod
    def _get_locale_key(self, data: str):
        return self.getClassNameJoined() + '.' + data
