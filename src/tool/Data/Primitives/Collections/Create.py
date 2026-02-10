from App.Objects.Act import Act
from App.Objects.Arguments.ArgumentDict import ArgumentDict
from App.Objects.Arguments.Argument import Argument
from App.Objects.Arguments.ListArgument import ListArgument
from App.Objects.Arguments.Assertions.NotNone import NotNone
from App.Objects.Responses.ObjectsList import ObjectsList
from Data.Types.String import String
from typing import ClassVar
from App import app

class Create(Act):
    type_that_creates: ClassVar[str] = 'Data.Primitives.Collections.Collection'

    @classmethod
    def _arguments(cls) -> ArgumentDict:
        return ArgumentDict(items = [
            ListArgument(
                name = 'name',
                orig = String,
                assertions = [NotNone()],
                allow_commas_fallback = False
            ),
            Argument(
                name = 'collection_type',
                orig = String,
                default = None
            )
        ])

    def _implementation(self, i):
        items = ObjectsList(items = [])
        for name in i.get('name'):
            type_that_creates = self.type_that_creates
            if i.get('collection_type') != None:
                type_that_creates = i.get('collection_type')

            _obj = app.ObjectsList.getByName(type_that_creates)
            assert _obj != None, 'module with name {0} not found'.format(type_that_creates)

            collection = _obj.getModule()()
            collection.local_obj.name = name

            self._creation_hook(collection, i)
            items.append(collection)

        return items

    def _creation_hook(self, collection, i):
        pass
