from App.Objects.Object import Object
from pydantic import Field
from typing import Any
from pathlib import Path
from App import app
import importlib

class NotAnObjectError(Exception):
    pass

class LoadedObject(Object):
    '''
    Filepath that may contain module
    '''

    path: str = Field()
    root: str = Field(default = None)

    title: str = None
    parts: list[str] = None
    _module: Any = None

    is_success: bool = False
    is_prioritized: bool = False
    is_submodule: bool = False

    def constructor(self):
        _path = Path(self.path)
        _ext = _path.suffix[1:] # its always "py", why moving it lol

        self.title = _path.stem
        self.parts = []
        for part in _path.parts:
            if f".{_ext}" in part:
                continue
            self.parts.append(part)

    def getModule(self):
        if self._module == None:
            self.setModule(self.loadModule(ignore_modules = True))

        return self._module

    def getTitle(self):
        return self.parts + [self.title]

    def getTitleWithClass(self):
        return self.parts + [self.title, self.title]

    def setModule(self, module):
        self._module = module

    def loadModule(self, ignore_modules: bool = False):
        module_name = ".".join(self.getTitle())

        _root = Path(self.root)
        _mod = _root.joinpath('\\'.join(self.parts))

        spec = importlib.util.spec_from_file_location(module_name, _mod.joinpath(self.title + '.py'))
        assert spec != None, 'spec not found'
        module = importlib.util.module_from_spec(spec)

        spec.loader.exec_module(module)

        common_object = getattr(module, self.title, None)
        assert common_object != None, f"{module_name}: {self.title} is not found"
        if ignore_modules == False and hasattr(common_object, 'getNotInstalledModules') == True:
            _modules = common_object.getNotInstalledModules()
            assert len(_modules) == 0, f"following modules not installed: {', '.join(_modules)}"

        try:
            if issubclass(common_object, Object) == False:
                raise NotAnObjectError(f"{module_name} probaly is not an Object")
        except TypeError:
            raise NotAnObjectError(f"{module_name} is not a class")

        return common_object

    def integrateModule(self, module) -> None:
        if app.Config != None:
            app.Config.appendSettingsOfModule(module)

        module.mount()

    @property
    def name(self) -> str:
        '''
        property to get DictList working
        '''

        return '.'.join(self.getTitleWithClass())
        if self._module == None:
            return '.'.join(self.getTitle())

        return self._module.getClassNameJoined()

    @property
    def is_inited(self) -> bool:
        return self._module != None
