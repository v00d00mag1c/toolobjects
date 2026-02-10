from App.Objects.Misc.DictList import DictList
from App.Objects.Object import Object
from App.Objects.Index.LoadedObject import LoadedObject
from App.Objects.Index.Namespaces.Namespace import Namespace
from App.Objects.Arguments.Argument import Argument
from App.Objects.Arguments.ListArgument import ListArgument
from Data.Types.Dict import Dict
from Data.Types.String import String
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
    names_redirects: dict[str, str] = Field(default = {})

    # cache
    _items: DictList = None
    _last_current: list[str] = None

    @classmethod
    def mount(cls):
        from App import app

        _objects = cls(
            namespaces = [
                app.app.objects
            ],
            current = cls.getOption("objects.index.namespaces.current"),
            names_redirects = cls.getOption("objects.index.redirects")
        )

        for item in cls.getOption('objects.index.namespaces'):
            _objects.append_namespace(item)
            item.load()

        app.mount('ObjectsList', _objects)

    def append_namespace(self, namespace: Namespace):
        self.namespaces.append(namespace)

    def get_namespace_with_name(self, name: str):
        for item in self.namespaces:
            if item.name == name:
                return item

    def has_namespace_with_name(self, name: str):
        return self.get_namespace_with_name(name) != None

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

    def getObjectsByCategory(self, category: list[str]) -> Generator[LoadedObject]:
        '''
        find by category:

        category="App.Objects" - returns all plugins from App\\Objects
        '''

        for item in self.getItems().toList():
            # TODO: add a better check
            if '.'.join(item.parts).startswith('.'.join(category)):
                yield item

    def getByName(self, key: str, class_name = None) -> LoadedObject:
        if key in self.names_redirects:
            key = self.names_redirects.get(key)

        _item = self.getItems().get(key)
        if class_name != None:
            if class_name != _item.self_name:
                return None

        return _item

    def sort(self, items: list[str]) -> dict:
        _items = dict()
        names = list()
        total_count = 0
        for item in items:
            _items[item.get_name_for_dictlist()] = item
            names.append(item.get_name_for_dictlist())

        categories = dict()

        # maybe it should be in xml?
        for _name in sorted(names):
            obj = _items.get(_name)
            name = obj.getTitle()

            cursor_link = categories
            ind = 0
            ind_max = len(name)

            # Yes, it would be better if it was written with xml, but ok. 
            # It creates hash table -> creates empty dicts in each category in name in common categories dict
            # , then if it the last part of the name - puts dict with last part of name and full name
            for item in name:
                if ind == ind_max - 1:
                    if cursor_link.get('_items') == None:
                        cursor_link['_items'] = []

                    total_count += 1
                    cursor_link.get('_items').append({
                        'part': item,
                        'obj': obj
                    })

                    continue

                if cursor_link.get(item) == None:
                    cursor_link[item] = {}
                cursor_link = cursor_link[item]

                ind += 1

        return categories, total_count

    @classmethod
    def _settings(cls):
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
            ),
            Argument(
                name = 'objects.index.redirects',
                default = {},
                orig = Dict
            )
        ]
