from App.Objects.Object import Object
from App.Data.Increment import Increment
from App.Data.DictList import DictList
from App import app
from pathlib import Path
from typing import Generator
from .LoadedObject import LoadedObject, NotAnObjectError
import traceback

class List(Object):
    id: Increment = None
    items: DictList = None
    calls: list = []
    priority_names: list = ['App\\Config\\Config.py', 'App\\Logger\\Logger.py', 'App\\Storage\\Storage.py', 'Web\\DownloadManager\\Manager.py']

    def constructor(self):
        self.id = Increment()
        self.items = DictList(items = [])

    def load(self, search_dir: Path):
        # traceback.print_list(traceback.extract_stack())

        self.log("Loading objects list...")
        _cached_names = []

        for item_path in self.scan(search_dir):
            plugin = LoadedObject.from_path(item_path)

            try:
                plugin.module = plugin.get_module()
                plugin.succeed_load()

            except NotAnObjectError:
                pass
            except Exception as e:
                plugin.failed_load(e)

            self.items.append(plugin)

            # Loading submodules
            if plugin.module != None:
                _cached_names.append(plugin.module.meta.class_name_joined)

                submodules = plugin.module.getAllSubmodules()
                for submodule in submodules:
                    name = submodule.module.meta.class_name_joined
                    if name in _cached_names:
                        continue

                    _obj = LoadedObject()
                    _obj.is_submodule = True
                    _obj.category = submodule.module.meta.class_name
                    _obj.title = submodule.module.__name__
                    _obj.module = submodule.module

                    _obj.succeed_load()

    def scan(self, path: Path) -> Generator[Path]:
        items: list = list()
        files = path.rglob('*.py')
        priority = [path.joinpath(p) for p in self.priority_names]

        # 1st iteration
        for plugin in files:
            # 2nd iteration
            if plugin not in priority:
                items.append(plugin)

        # adding priority and plugins that are not in priority. Maybe its better to do sort there*?
        for plugin in priority + items:
            # Hardcoded check. should be changed
            if plugin.name in ['', '__pycache__', 'Base.py', 'tool.py', '.gitkeep']:
                continue

            yield plugin.relative_to(path)

    def getListBySelfName(self, class_name = None) -> list[LoadedObject]:
        output = []
        for item_name, item in self.items.items():
            if class_name != None:
                if class_name != item.self_name:
                    continue

            output.append(item)

        return output

    def getByName(self, key: str, class_name = None) -> LoadedObject:
        _item = self.items.get(key)

        if class_name != None:
            if class_name != _item.self_name:
                return None

        return _item

    def getList(self) -> list:
        return self.items.items
