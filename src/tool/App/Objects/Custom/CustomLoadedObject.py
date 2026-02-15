from App.Objects.Index.LoadedObject import LoadedObject
from App.Storage.StorageUUID import StorageUUID
from App import app
from pydantic import Field

class CustomLoadedObject(LoadedObject):
    id: StorageUUID = Field(default = None)

    def init_hook(self):
        obj = self.id.toPython()
        names = obj.name.split('.')

        self.title = names[-1]
        self.object_name = self.title
        self.parts = names[:-1]

    def loadModule(self, ignore_requires: bool = False):
        obj = self.id.toPython()

        _mro = list()

        for item in obj.extends_from:
            _module = app.ObjectsList.getByName(item)
            _mro.append(_module.getModule())

        new = type(self.object_name, tuple(_mro), {
            '__module__': self.get_name_for_dictlist()
        })

        if obj.arguments != None:
            @classmethod
            def _arg_func(cls):
                return obj.arguments

            new._arguments = _arg_func

        if obj.submodules != None:
            @classmethod
            def _submodules_func(cls):
                return obj.submodules

            new._submodules = _submodules_func

        if obj.execution != None:
            async def _implementation(self, i):
                return await obj.execution.run(i)

            new._implementation = _implementation

        return new

    def unloadModule(self):
        if self._module == None:
            return

        #_name = self._module._getClassNameJoined()
