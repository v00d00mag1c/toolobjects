from App.Objects.Act import Act
from App.Arguments.ArgumentDict import ArgumentDict
from App.Arguments.Objects.Literal import Literal
from App.Arguments.Objects.List import List
from App.Arguments.Types.String import String
from App.Arguments.Types.Int import Int
from App.Storage.Storage import StorageArgument
from App.Arguments.Assertions.NotNoneAssertion import NotNoneAssertion
from App.Responses.AnyResponse import AnyResponse

class Link(Act):
    @classmethod
    def getArguments(cls):
        return ArgumentDict(items = [
            StorageArgument(
                name = 'storage',
                assertions = [NotNoneAssertion()]
            ),
            Int(
                name = 'owner',
                assertions = [NotNoneAssertion()]
            ),
            List(
                name = 'items',
                assertions = [NotNoneAssertion()],
                orig = Int(
                    name = 'item'
                ),
                default = []
            ),
            Literal(
                name = 'act',
                default = 'link',
                values = [
                    String(
                        name = 'link'
                    ),
                    String(
                        name = 'unlink'
                    )
                ]
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
