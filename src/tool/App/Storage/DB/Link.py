from App.Objects.Act import Act
from Data.Int import Int
from Data.String import String
from Data.Int import Int
from App.Objects.Arguments.ArgumentDict import ArgumentDict
from App.Objects.Arguments.Argument import Argument
from App.Objects.Arguments.LiteralArgument import LiteralArgument
from App.Objects.Arguments.Assertions.NotNoneAssertion import NotNoneAssertion
from App.Responses.AnyResponse import AnyResponse
from App.Storage.StorageItem import StorageItem

class Link(Act):
    @classmethod
    def getArguments(cls):
        return ArgumentDict(items = [
            Argument(
                name = 'storage',
                orig = StorageItem,
                assertions = [NotNoneAssertion()]
            ),
            Argument(
                name = 'owner',
                orig = Int,
                assertions = [NotNoneAssertion()]
            ),
            Argument(
                name = 'items',
                orig = Int,
                assertions = [NotNoneAssertion()],
                default = []
            ),
            LiteralArgument(
                name = 'act',
                default = 'link',
                values = ['link', 'unlink']
            )
        ])

    async def implementation(self, i):
        _storage = i.get('storage')

        assert _storage != None, f"storage {_storage.name} not found"
        assert _storage.hasAdapter(), f"storage {_storage.name} does not contains db connection"

        # TODO Fix
        link_to = _storage.adapter.ObjectAdapter.getById(i.get('owner'))
        items = _storage.adapter.ObjectAdapter.getByIds(i.get('items'))

        for item in items:
            _f = link_to.toPython()
            _s = item.toPython()

            match (i.get('act')):
                case 'link':
                    _f.link(_s)
                case 'unlink':
                    _f.unlink(_s)

            self.log(f"{i.get('act')}ed {_f.getDbId()} and {_s.getDbId()}")
