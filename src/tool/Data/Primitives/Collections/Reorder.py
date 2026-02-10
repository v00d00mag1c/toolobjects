from App.Objects.Act import Act
from App.Objects.Object import Object
from App.Objects.Arguments.ArgumentDict import ArgumentDict
from App.Objects.Arguments.Argument import Argument
from App.Objects.Arguments.Assertions.NotNone import NotNone
from Data.Primitives.Collections.Collection import Collection
from App.DB.SwapLinks import SwapLinks

class Reorder(Act):
    @classmethod
    def _arguments(cls) -> ArgumentDict:
        return ArgumentDict(
            items = [
                Argument(
                    name = 'collection',
                    by_id = True,
                    assertions = [NotNone()],
                    orig = Collection,
                ),
                Argument(
                    name = 'item_1',
                    by_id = True,
                    assertions = [NotNone()],
                    orig = Object,
                ),
                Argument(
                    name = 'item_2',
                    by_id = True,
                    assertions = [NotNone()],
                    orig = Object,
                )
            ]
        )

    async def implementation(self, i):
        collection = i.get('collection')
        item_1 = i.get('item_1')
        item_2 = i.get('item_2')

        _link1 = collection.find_link(item_1)
        _link2 = collection.find_link(item_2)

        return await SwapLinks().execute({
            'uuid1': _link1.getDbIds(),
            'uuid2': _link2.getDbIds(),
        })
