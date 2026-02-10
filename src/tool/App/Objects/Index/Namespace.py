from App.Objects.Object import Object
from App.Objects.Index.LoadedObject import LoadedObject, NotAnObjectError
from App.Objects.DictList import DictList
from typing import Generator
from pathlib import Path
from pydantic import Field
import sys

class Namespace(Object):
    '''
    Represents dir from which the object classes will be loaded

    name: id of the namespace
    root: dir 
    load_before, load_after: will loaded only before or after any other objects
    '''

    _names: list[str] = []
    name: str = Field()
    root: str = Field()
    load_before: list = Field(default = [])
    load_after: list = Field(default = [])
    ignore_dirs: list = Field(default = [])
    load_once: bool = Field(default = True)

    items: DictList = Field(default = None)

    def constructor(self):
        self.items = DictList(items=[])

        # Allows to import objects from other namespaces
        _root = str(self.root)
        if _root not in sys.path:
            sys.path.append(_root)

    def load(self):
        for item in self.scan():
            try:
                assert self.verify(item)
                assert self.isAlreadyLoaded(item) == False

                self._names.append(item.name)

                if self.load_once == True or item.is_prioritized == True:
                    _module = item.loadModule()
                    item.setModule(_module)
                    item.integrateModule(_module)

                    item.is_success = True

                    self.noticeModuleLoaded(item)
                else:
                    self.log(f"{item.name}: loaded but not imported", role=['module_skipped'])
            except AssertionError:
                pass
            except Exception as exception:
                item.is_success = False
                self.log_error(exception)

                if isinstance(exception, AssertionError) == False and isinstance(exception, ModuleNotFoundError) == False and isinstance(exception, NotAnObjectError) == False:
                    raise exception

            self.items.append(item)

    def scan(self) -> Generator[LoadedObject]:
        '''
        Scans self.root and returns as Generator
        '''

        # Wont output because Logger is not loaded at this moment
        # TODO not load from Custom
        self.log(f"Namespace {self.name}, loading objects from dir {self.root}")

        global_path = Path(self.root)
        _side_names = ['', '__init__.py', '__pycache__', 'Base.py', 'tool.py', '.gitkeep']

        for plugin in self.load_before:
            plugin.is_prioritized = True
            plugin.root = self.root

            yield plugin

        files = global_path.rglob('*.py')
        for plugin in files:
            _path = plugin.relative_to(global_path)
            _str_path = str(_path)
            _skip = False
            for _ignore in self.ignore_dirs:
                if _str_path.startswith(_ignore):
                    _skip = True

            if plugin.name in _side_names:
                _skip = True

            for item in self.load_after:
                if item.path == _str_path:
                    _skip = True
            if _skip == True:
                continue

            # "ignore_dirs" param

            yield LoadedObject(
                path = _str_path,
                root = self.root
            )

        for plugin in self.load_after:
            plugin.is_prioritized = True
            plugin.root = self.root

            yield plugin

    def verify(self, module: LoadedObject):
        '''
        If it notices that module's hash not found (where we will take hashes? from github file?) does not allows to import
        '''
        return True

    def getByName(self, key: str, class_name: str = None) -> LoadedObject:
        _item = self.items.get(key)
        if class_name != None:
            if class_name != _item.self_name:
                return None

        return _item

    def getItems(self) -> list:
        return self.items.items

    def noticeModuleLoaded(self, item: LoadedObject):
        _role = []
        if item.is_prioritized:
            _role.append('priority')
        if item.is_submodule:
            _role.append('submodule')

        self.log(f"{item.getModule().self_name.lower()} {item.name}: loaded and imported", role=_role)

    def isAlreadyLoaded(self, item: LoadedObject) -> bool:
        return item.name in self._names

    @property
    def append_prefix(self): # -> LogPrefix
        return {'name': 'Namespace', 'id': self.name}
