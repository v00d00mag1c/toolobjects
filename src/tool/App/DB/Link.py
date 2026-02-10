from App.Objects.Act import Act
from Data.Types.Int import Int
from Data.Types.String import String
from App.Objects.Arguments.ArgumentDict import ArgumentDict
from App.Objects.Arguments.Argument import Argument
from App.Objects.Arguments.LiteralArgument import LiteralArgument
from App.Objects.Arguments.ListArgument import ListArgument
from App.Objects.Arguments.Assertions.NotNone import NotNone
from App.Storage.StorageUUID import StorageUUID

class Link(Act):
    @classmethod
    def _arguments(cls):
        return ArgumentDict(items = [
            Argument(
                name = 'owner',
                orig = StorageUUID,
                assertions = [NotNone()]
            ),
            ListArgument(
                name = 'items',
                orig = StorageUUID,
                assertions = [NotNone()],
                default = []
            ),
            LiteralArgument(
                name = 'act',
                default = 'link',
                orig = String,
                values = ['link', 'unlink']
            ),
            ListArgument(
                name = 'role',
                orig = String,
                assertions = [NotNone()],
                default = []
            ),
        ])

    async def _implementation(self, i):
        # TODO Fix
        link_to = i.get('owner').getItem()
        _items = list()

        for item in i.get('items'):
            _items.append(item.uuid)

        items = link_to._adapter.ObjectAdapter.getByIds(_items)
        _role = i.get('role')

        for item in items:
            _f = link_to.toPython()
            _s = item.toPython()

            match (i.get('act')):
                case 'link':
                    _f.link(_s, _role)
                case 'unlink':
                    _f.unlink(_s, _role)

            self.log("{0}ed {1} and {2}".format(i.get('act'), _f.getDbId(), _s.getDbId()))
