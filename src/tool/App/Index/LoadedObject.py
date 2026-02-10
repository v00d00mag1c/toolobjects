from App.Objects.Object import Object
from typing import Any
from pathlib import Path
import importlib

class LoadedObject(Object):
    is_success: bool = False
    is_submodule: bool = False

    title: str = None
    category: list[str] = None
    module: Any = None

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
        self.log(f"Loaded object {self.module.meta.name_joined}")

    def failed_load(self, exception: Exception):
        self.is_success = False
        self.log_error(exception)

        if isinstance(exception, AssertionError) == False:
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
            assert issubclass(common_object, Object), f"{module_name} probaly is not an Object"
        except TypeError:
            raise AssertionError(f"{module_name} is not a class")

        try:
            common_object.hooks.trigger('loaded')
        except:
            pass

        return common_object

    def verify_module_hash(self, module_name: str) -> bool:
        return True
