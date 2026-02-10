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
    priority_names: list = [
        'App\\Storage\\Config.py', 
        'App\\Logger\\Logger.py', 
        'App\\Storage\\Storage.py', 
        'Web\\DownloadManager\\Manager.py'
    ]

    def constructor(self):
        self.id = Increment()
        self.items = DictList(items = [])

    def load(self, search_dir: Path):
        # traceback.print_list(traceback.extract_stack())

        # It will never show because Logger is not loaded and mounted at this moment :))
        self.log("Loading objects list")
        _cached_names = []

        for plugin in self.scan(search_dir):
            if plugin.is_prioritized == True:
                plugin.selfInit()

            self.items.append(plugin)

            # Loading submodules
            if plugin.getModule() != None:
                _cached_names.append(plugin.getModule().getClassNameJoined())

                for submodule in plugin.getModule().getAllSubmodules():
                    name = submodule.item.getClassNameJoined()
                    if name in _cached_names:
                        continue

                    _obj = LoadedObject()
                    _obj.is_submodule = True
                    _obj.category = submodule.item.getClassName()
                    _obj.title = submodule.item.__name__
                    _obj._module = submodule.item

                    _obj.succeed_load()

    def scan(self, path: Path) -> Generator[Path]:
        _side_names = ['', '__pycache__', 'Base.py', 'tool.py', '.gitkeep']
        files = path.rglob('*.py')
        priority = [path.joinpath(p) for p in self.priority_names]

        for plugin in priority:
            _plugin = LoadedObject.from_path(plugin.relative_to(path))
            _plugin.is_prioritized = True

            yield _plugin

        for plugin in files:
            if plugin.name not in _side_names and plugin not in priority:
                yield LoadedObject.from_path(plugin.relative_to(path))

    def getObjectsByNamespace(self, category: list[str]) -> Generator[LoadedObject]:
        '''
        find by category:

        category="App.Objects" - returns all plugins from App\\Objects
        '''
        for item in self.items:
            if '.'.join(item.category).startswith(category):
                yield item

    def getByName(self, key: str, class_name = None) -> LoadedObject:
        _item = self.items.get(key)
        if class_name != None:
            if class_name != _item.self_name:
                return None

        return _item

    def getList(self) -> list:
        return self.items.items
