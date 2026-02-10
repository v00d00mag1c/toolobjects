from App.Objects.Object import Object
from pydantic import Field, computed_field
from typing import Any
from pathlib import Path
from App import app
from functools import cached_property
from App.Objects.Index.ModuleData import ModuleData
import importlib, sys

class NotAnObjectError(Exception):
    pass

class LoadedObject(Object):
    '''
    Filepath that may contain module
    '''

    path: str = Field()
    root: str = Field(default = None)

    title: str = None
    object_name: str = None
    parts: list[str] = None
    _module: Any = None

    is_success: bool = False
    is_prioritized: bool = False
    is_submodule: bool = False
    mounted: bool = False

    def constructor(self):
        _path = Path(self.path)
        _ext = _path.suffix[1:] # its always "py", why moving it lol

        self.title = _path.stem
        self.object_name = self.title
        self.parts = []
        for part in _path.parts:
            if f".{_ext}" in part:
                continue
            self.parts.append(part)

    def getModule(self):
        if self._module == None:
            self.setModule(self.loadModule(ignore_requires = True))
            self.integrateModule(self._module)

        return self._module

    def hasModuleLoaded(self):
        return self._module != None

    def getTitle(self):
        return self.parts + [self.title]

    def getTitleWithClass(self):
        # to not double
        if self.title == self.object_name:
            return self.parts + [self.title]

        return self.parts + [self.title, self.object_name]

    def setModule(self, module):
        self._module = module

    def loadModule(self, ignore_requires: bool = False):
        module_name = ".".join(self.getTitle())

        _root = Path(self.root)
        _mod = _root.joinpath('\\'.join(self.parts))

        spec = importlib.util.spec_from_file_location(module_name, _mod.joinpath(self.title + '.py'))
        assert spec != None, 'spec not found'
        module = importlib.util.module_from_spec(spec)

        spec.loader.exec_module(module)

        common_object = getattr(module, self.title, None)
        assert common_object != None, f"{module_name}: {self.title} is not found"
        if ignore_requires == False and hasattr(common_object, 'getNotInstalledModules') == True:
            _modules = common_object.getNotInstalledModules()
            assert len(_modules) == 0, f"following modules not installed: {', '.join(_modules)}"

        try:
            if issubclass(common_object, Object) == False:
                raise NotAnObjectError(f"{module_name} probaly is not an Object")
        except TypeError:
            raise NotAnObjectError(f"{module_name} is not a class")

        return common_object

    def unloadModule(self):
        if self._module == None:
            return

        _name = self._module.getClassNameJoined()
        if _name in sys.modules:
            sys.modules.pop(_name)

    def integrateModule(self, module) -> None:
        if app.Config != None:
            self.appendSettings()

        if self.mounted == False:
            self.mounted = True
            module.mount()

    def appendSettings(self) -> None:
        _settings = self.getModule().getSettings()
        for _item in _settings:
            app.Config.getItem(role = _item.role).append_compare(_item)

    @computed_field
    @property
    def name(self) -> str:
        '''
        property to get DictList working
        '''

        return '.'.join(self.getTitleWithClass())

        return self._module.getClassNameJoined()

    @property
    def is_inited(self) -> bool:
        return self._module != None

    @computed_field
    @property
    def module(self) -> ModuleData:
        if self.hasModuleLoaded() == False:
            return None

        return ModuleData.from_module(self.getModule(), include_subs = True, include_args = True, include_settings = True, include_requirements = True, include_variables = True)
