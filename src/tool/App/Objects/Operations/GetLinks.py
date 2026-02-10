from App.Objects.Act import Act
from App.Objects.Object import Object
from Data.Types.Boolean import Boolean
from App.Objects.Arguments.ArgumentDict import ArgumentDict
from App.Objects.Arguments.Argument import Argument
from App.Objects.Arguments.Assertions.NotNone import NotNone
from App.Objects.Responses.ObjectsList import ObjectsList

class GetLinks(Act):
    @classmethod
    def _arguments(cls) -> ArgumentDict:
        return ArgumentDict(items = [
            Argument(
                name = 'item',
                by_id = True,
                orig = Object,
                assertions = [NotNone()]
            ),
            Argument(
                name = 'ignore_virtual',
                orig = Boolean,
                default = False
            )
        ])

    def _implementation(self, i):
        _list = ObjectsList(items = [], unsaveable = True)

        for link in i.get('item').getLinked(i.get('ignore_virtual')):
            _list.append(link)

        return _list
