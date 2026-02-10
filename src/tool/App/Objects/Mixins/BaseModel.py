from typing import Any
from App.Objects.Misc.ObjectMeta import ObjectMeta
from App.Objects.Misc.LocalObjectMeta import LocalObjectMeta
from App.Objects.Misc.SavedVia import SavedVia
from App.Objects.Mixins.Section import Section
from App.Objects.Mixins.Model import Model
from pydantic import Field, model_validator, computed_field

class BaseModel(Model, Section):
    obj: ObjectMeta = Field(default = ObjectMeta())
    local_obj: LocalObjectMeta = Field(default = LocalObjectMeta())

    @model_validator(mode='after')
    def _saved_via(self):
        self.obj.saved_via = SavedVia()
        self.obj.saved_via.object_name = self._getClassNameJoined()

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

    @classmethod
    def _get_locale_key(self, data: str):
        return self._getClassNameJoined() + '.' + data

    def _get_name(self) -> str:
        return self._getNameJoined()

    @computed_field
    @property
    def any_name(self) -> str:
        if self.local_obj.name:
            return self.local_obj.name
        if self.obj.name:
            return self.obj.name

        return self._get_name()
