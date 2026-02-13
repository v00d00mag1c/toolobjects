from typing import Any
from App.Objects.Misc.ObjectMeta import ObjectMeta
from App.Objects.Misc.LocalObjectMeta import LocalObjectMeta
from App.Objects.Misc.SavedVia import SavedVia
from App.Objects.Mixins.Model import Model
from pydantic import Field, model_validator, computed_field

class BaseModel(Model):
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

    def _get_fields(self) -> dict:
        _res = dict()
        for key, item in self.to_json().items():
            if type(item) in [dict, list]:
                pass

            _res[key] = item

        return _res

    @computed_field
    @property
    def any_name(self) -> str:
        if self.local_obj.name:
            return self.local_obj.name
        if self.obj.name:
            return self.obj.name

        return self._get_name()

    @computed_field
    @property
    def any_description(self) -> str:
        if self.local_obj.description:
            return self.local_obj.description
        if self.obj.description:
            return self.obj.description

        return ''

    @classmethod
    def get_creations(cls) -> list:
        return []

    def add_thumbnail(self, item: Model):
        self.link(item, role = ['thumbnail'])

    def add_thumbnails(self, items):
        for item in items:
            self.add_thumbnail(item)

    def get_thumbnails(self, include_linked: bool = True):
        #for thumb in self.local_obj.thumbnail:
        #    thumb.setDb(self.getDb())

        #    yield thumb

        for thumb in self.getLinked(with_role = 'thumbnail'):
            yield thumb
