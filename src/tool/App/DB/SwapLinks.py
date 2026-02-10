from App.Objects.Act import Act
from App.Objects.Arguments.ArgumentDict import ArgumentDict
from App.Objects.Arguments.Argument import Argument
from App.Objects.Arguments.Assertions.NotNone import NotNone
from App.Storage.StorageUUID import StorageUUID

class SwapLinks(Act):
    @classmethod
    def _arguments(cls) -> ArgumentDict:
        return ArgumentDict(items = [
            Argument(
                name = 'uuid1',
                orig = StorageUUID,
                assertions = [NotNone()]
            ),
            Argument(
                name = 'uuid2',
                orig = StorageUUID,
                assertions = [NotNone()]
            )
        ])

    async def implementation(self, i):
        id1 = i.get('uuid1')
        id2 = i.get('uuid2')
        id1.model_name = 'link'
        id2.model_name = 'link'

        _item1 = id1.getItem()
        _item2 = id2.getItem()

        assert _item1 != None and _item2 != None, 'one of the link is not found'
        assert _item1.getStorageItemName() == _item2.getStorageItemName(), 'cross-db'

        _id2_order = int(_item2.order)
        _id1_order = int(_item1.order)
        _item1.reorder(_id2_order)
        _item2.reorder(_id1_order)
