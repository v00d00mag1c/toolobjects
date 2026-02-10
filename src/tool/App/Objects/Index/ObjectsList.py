from App.Objects.DictList import DictList
from App.Objects.Object import Object
from App.Objects.Index.LoadedObject import LoadedObject
from App.Objects.Index.Namespace import Namespace
from typing import Generator
from App import app
from pydantic import Field

class ObjectsList(Object):
    '''
    All the Namespaces of the app, functions to switch between them

    current: ids (names) of used namespaces
    '''

    namespaces: list[Namespace] = Field()
    current: list[str] = Field(default = ['common'])

    # cache
    _items: DictList = None
    _last_current: list[str] = None

    @classmethod
    def mount(cls):
        from App import app

        _objects = cls(
            namespaces = [
                app.app.objects
            ]
        )

        for item in cls.getOption('objects.index.namespaces'):
            _objects.namespaces.append(item)

        app.mount('ObjectsList', _objects)

    def getItems(self) -> DictList:
        if self._last_current != None and self._last_current == self.current:
            return self._items

        self._items = DictList(items=[])
        for item in self.namespaces:
            if item.name in self.current:
                for object_item in item.getItems():
                    self._items.append(object_item)

        self._last_current = self.current

        return self._items

    def getObjectsByGroup(self, category: list[str]) -> Generator[LoadedObject]:
        '''
        find by category:

        category="App.Objects" - returns all plugins from App\\Objects
        '''

        for item in self.getItems().toList():
            # TODO: add a better check
            if '.'.join(item.parts).startswith('.'.join(category)):
                yield item

    def getByName(self, key: str, class_name = None) -> LoadedObject:
        _item = self.getItems().get(key)
        if class_name != None:
            if class_name != _item.self_name:
                return None

        return _item

    @classmethod
    def getSettings(cls):
        from App.Arguments.Objects.List import List
        from App.Arguments.Objects.Orig import Orig

        return [
            List(
                name = 'objects.index.namespaces',
                default = [],
                orig = Orig(
                    name = 'objects.index.namespace',
                    orig = Namespace
                )
            )
        ]
