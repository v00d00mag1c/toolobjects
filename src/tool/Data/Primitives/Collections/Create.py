from App.Objects.Act import Act
from App.Objects.Arguments.ArgumentDict import ArgumentDict
from App.Objects.Arguments.Argument import Argument
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
            Argument(
                name = 'name',
                orig = String,
                assertions = [NotNone()]
            )
        ])

    def _implementation(self, i):
        name = i.get('name')

        _obj = app.ObjectsList.getByName(self.type_that_creates)
        collection = _obj.getModule()()
        collection.local_obj.name = name

        return ObjectsList(items = [collection])
