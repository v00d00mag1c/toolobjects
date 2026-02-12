from App.Objects.Act import Act
from App.Objects.Arguments.ArgumentDict import ArgumentDict
from App.Objects.Arguments.Argument import Argument
from App.Storage.Item.StorageItem import StorageItem
from App.DB.Query.Condition import Condition
from App.DB.Query.Values.Value import Value

class ClearTemp(Act):
    @classmethod
    def _arguments(cls) -> ArgumentDict:
        return ArgumentDict(items = [
            Argument(
                name = 'storage',
                default = 'tmp',
                orig = StorageItem
            )
        ])

    async def _implementation(self, i):
        storage = i.get('storage')
        query = storage.adapter.getQuery()
        query.addCondition(Condition(
            val1 = Value(
                column = 'content',
                json_fields = ['obj', 'is_tmp'],
            ),
            operator = '==',
            val2 = Value(
                value = True
            )
        ))

        for item in query.toObjectsList().getItems():
            item.delete(remove_links = True)

        storage.adapter.commit()
