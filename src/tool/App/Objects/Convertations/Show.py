from App.Objects.Act import Act
from App.Objects.Object import Object
from App.Objects.Arguments.ArgumentDict import ArgumentDict
from App.Objects.Arguments.Argument import Argument
from App.Objects.Arguments.Assertions.NotNone import NotNone
from App.Objects.Responses.ObjectsList import ObjectsList

class Show(Act):
    @classmethod
    def _arguments(cls) -> ArgumentDict:
        return ArgumentDict(items = [
            Argument(
                name = 'from',
                by_id = True,
                orig = Object,
                assertions = [NotNone()]
            )
        ])

    async def _implementation(self, i):
        _list = ObjectsList()
        for submodule in i.get('from').getSubmodules(with_role=['convertation']):
            _list.append(submodule)

        return _list
