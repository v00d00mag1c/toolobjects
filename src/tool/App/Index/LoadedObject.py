from App.Objects.Object import Object
from typing import Any
from pathlib import Path
from App import app
import importlib

class NotAnObjectError(Exception):
    pass

class LoadedObject(Object):
    is_success: bool = False
    is_prioritized: bool = False
    is_submodule: bool = False

    title: str = None
    _module: Any = None
    _attempt_to_name: str = None

    category: list[str] = None

    def getModule(self):
        #self.log('getModule called')
        if self._module == None:
            self.selfInit()

        return self._module

    def selfInit(self):
        try:
            self._module = self.load_module()

            # It's strange to put log function to class internals
            self.succeed_load()
        except NotAnObjectError:
            pass
        except Exception as e:
            self.failed_load(e)

    @property
    def name(self) -> str:
        '''
        property to get DictList working
        '''
        #self.log('object.name called')
        if self._module == None:
            return self._attempt_to_name
            #return '_____' + self.title #don't remember why

        return self._module.getClassNameJoined()

    @staticmethod
    def from_path(path: Path):
        plugin = LoadedObject()

        plugin.title = path.stem
        plugin.category = []

        ext = path.suffix[1:]

        for part in path.parts:
            if f".{ext}" in part:
                continue

            plugin.category.append(part)

        plugin._attempt_to_name = '.'.join(plugin.category + [plugin.title, plugin.title])

        return plugin

    def succeed_load(self):
        self.is_success = True

        _appends = []
        if self.is_prioritized:
            _appends.append('(!)')
        if self.is_submodule:
            _appends.append('(submodule)')

        self.log(f"Loaded {self._module.self_name.lower()} {self._module.getClassNameJoined()} {" ".join(_appends)}")

    def failed_load(self, exception: Exception):
        self.is_success = False
        self.log_error(exception)

        if isinstance(exception, AssertionError) == False and isinstance(exception, ModuleNotFoundError) == False:
            raise exception

    def load_module(self):
        parts = self.category + [self.title]
        module_name = ".".join(parts)

        assert self.verify_module_hash(module_name), f"module {module_name} not verified"

        _module = importlib.import_module(module_name)
        assert _module != None, f"module {module_name} not found"

        common_object = getattr(_module, self.title, None)
        assert common_object != None, f"{module_name}: {self.title} is not found"

        try:
            if issubclass(common_object, Object) == False:
                raise NotAnObjectError(f"{module_name} probaly is not an Object")
        except TypeError:
            raise NotAnObjectError(f"{module_name} is not a class")

        try:
            # Hook cannot be triggered for all class, so ive added "mount" hack
            #common_object.triggerHooks('loaded')

            if app.Config != None:
                # if config already exists (we loading it firstly), getting settings of the object (probaly getAllSettings needed here) and appendig to global config
                _settings = common_object.getSettings()
                if _settings != None:
                    for item in _settings:
                        app.Config.comparer.compare.append(item)

            common_object.mount()
        except Exception as e:
            raise e
            self.log_error(e, exception_prefix = "exception when importing: ")

        return common_object

    def verify_module_hash(self, module_name: str) -> bool:
        return True
