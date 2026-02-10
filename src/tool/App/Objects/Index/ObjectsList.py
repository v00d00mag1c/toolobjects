from App.Objects.Misc.DictList import DictList
from App.Objects.Object import Object
from App.Objects.Index.LoadedObject import LoadedObject
from App.Objects.Index.Namespace import Namespace
from App.Objects.Arguments.Argument import Argument
from App.Objects.Arguments.ListArgument import ListArgument
from App.Objects.Displayment import Displayment
from Data.String import String
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

        _custom = [
            Namespace(
                name = 'custom',
                root = str(app.app.cwd.joinpath('Custom'))
            )
        ]
        _objects = cls(
            namespaces = [
                app.app.objects
            ],
            current = cls.getOption("objects.index.namespaces.current")
        )

        for item in _custom + cls.getOption('objects.index.namespaces'):
            _objects.namespaces.append(item)
            item.load()

        app.mount('ObjectsList', _objects)

    def getItems(self, check_namespaces: bool = True) -> DictList:
        if self._last_current != None and self._last_current == self.current:
            return self._items

        self._items = DictList(items=[])
        for item in self.namespaces:
            if check_namespaces == True:
                if item.name not in self.current:
                    continue

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
    def getDisplayments(cls):
        return [Displayment(
            role = ['js'],
            value = "Web/_js/ObjectsList.js"
        )]

    @classmethod
    def getSettings(cls):
        return [
            ListArgument(
                name = 'objects.index.namespaces',
                default = [],
                orig = Namespace
            ),
            ListArgument(
                name = 'objects.index.namespaces.current',
                default = ['common'],
                orig = String
            )
        ]
