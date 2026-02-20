from typing import Any
from App.Objects.Misc.ObjectMeta import ObjectMeta
from App.Objects.Misc.LocalObjectMeta import LocalObjectMeta
from App.Objects.Misc.SavedVia import SavedVia
from App.Objects.Mixins.Model import Model
from pydantic import Field, model_validator, computed_field
from App import app

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

    def _get_fields(self) -> dict:
        _res = dict()
        for key, item in self.to_json().items():
            if type(item) in [dict, list]:
                pass

            _res[key] = item

        return _res

    async def _execute(self, object_name: str, args: dict = {}, executor_wheel: bool = True, auth_from_self: bool = True, do_save: bool = False, in_thread: bool = True):
        from App.Objects.Threads.ExecutionThread import ExecutionThread

        if auth_from_self and hasattr(self, 'auth'):
            args.update({
                'auth': self.auth,
            })

        if do_save == False:
            args.update({
                'do_save': 0
            })

        if executor_wheel:
            args.update({
                'i': object_name,
            })

            object_name = 'App.Objects.Operations.DefaultExecutorWheel'

        obj = app.ObjectsList.getByName(object_name)

        assert obj != None, 'object does not exist'

        executable = obj.getModule()()

        if in_thread:
            thread = ExecutionThread(id = -3)
            thread.set(executable.execute(args))
            thread.set_name(str(args.get('i')))
            results = await thread.get()
            thread.end()

            return results

        return await executable.execute(args)

    @classmethod
    def _creations(cls) -> list:
        return []

    @classmethod
    def get_creations(cls) -> list:
        exist_names = list()
        _list = list()
        for _class in cls.getMRO():
            if hasattr(_class, '_creations'):
                new_creations = _class._creations()
                if new_creations == None:
                    continue

                for creation in new_creations:
                    if creation.object_name in exist_names:
                        continue

                    exist_names.append(creation.object_name)
                    _list.append(creation)

        return _list
