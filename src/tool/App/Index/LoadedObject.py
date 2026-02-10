from App.Objects.Object import Object
from typing import Any
from pathlib import Path
import importlib

class NotAnObjectError(Exception):
    pass

class LoadedObject(Object):
    is_success: bool = False
    is_submodule: bool = False

    title: str = None
    category: list[str] = None
    module: Any = None

    @property
    def name(self) -> str:
        '''
        property to get DictList working
        '''

        if self.module == None:
            return '_____' + self.title

        return self.module.meta.class_name_joined

    @staticmethod
    def from_path(path: Path):
        plugin = LoadedObject()

        plugin.title = path.stem
        ext = path.suffix[1:]
        all_parts = path.parts
        plugin.category = []
        for part in all_parts:
            if f".{ext}" in part:
                continue

            plugin.category.append(part)

        return plugin

    def succeed_load(self):
        self.is_success = True
        self.log(f"Loaded {self.module.self_name.lower()} {self.module.meta.class_name_joined}")

    def failed_load(self, exception: Exception):
        self.is_success = False
        self.log_error(exception)

        if isinstance(exception, AssertionError) == False and isinstance(exception, ModuleNotFoundError) == False:
            raise exception

    def get_module(self):
        parts = self.category + [self.title]
        module_name = ".".join(parts)
        self.verify_module_hash(module_name)

        module = importlib.import_module(module_name)
        assert module != None, f"module {module_name} not found"

        common_object = getattr(module, self.title, None)
        assert common_object != None, f"{module_name}: {self.title} is not found"

        try:
            if issubclass(common_object, Object) == False:
                raise NotAnObjectError(f"{module_name} probaly is not an Object")
        except TypeError:
            raise NotAnObjectError(f"{module_name} is not a class")

        try:
            common_object.hooks.trigger('loaded')

            # hack to mount singletone. Must be moved to 'hooks'
            if hasattr(common_object, 'mount') == True:
                common_object.mount()
        except Exception as e:
            print(e)
            self.log(e, exception_prefix = "exception when importing: ")

        return common_object

    def verify_module_hash(self, module_name: str) -> bool:
        return True
