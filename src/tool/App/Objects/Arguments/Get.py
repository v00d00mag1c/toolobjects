from App.Objects.Act import Act
from App.Objects.Object import Object
from App.Objects.Arguments.Assertions.NotNone import NotNone
from App.Objects.Arguments.ArgumentDict import ArgumentDict
from App.Objects.Arguments.Argument import Argument
from App.Objects.Responses.ObjectsList import ObjectsList

class Get(Act):
    @classmethod
    def _arguments(cls) -> ArgumentDict:
        return ArgumentDict(items = [
            Argument(
                name = 'object',
                orig = Object,
                assertions = [NotNone()]
            )
        ])

    async def _implementation(self, i):
        _items = ObjectsList(unsaveable = True, supposed_to_be_single = True)
        _obj = i.get('object')
        for arg in _obj.getArguments().iterate():
            _items.append(arg)

        return _items
