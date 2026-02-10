from App.Objects.Act import Act
from App.Objects.Arguments.ArgumentDict import ArgumentDict
from App.Objects.Arguments.Argument import Argument
from App.Objects.Arguments.Assertions.NotNone import NotNone
from App.Objects.Responses.ObjectsList import ObjectsList
from Data.Boolean import Boolean

class Delete(Act):
    @classmethod
    def _arguments(cls) -> ArgumentDict:
        return ArgumentDict(items = [
            Argument(
                name = 'items',
                orig = ObjectsList,
                assertions = [NotNone()]
            ),
            Argument(
                name = 'remove_links',
                orig = Boolean,
                default = True
            )
        ])

    async def _implementation(self, i):
        _items = i.get('items')
        _index = 0
        for item in _items.getItems():
            if item == None:
                self.log('deletion items, index {0}: none!'.format(_index))
                continue

            self.log('deleting item {0}'.format(item.db_info))
            item.delete(i.get('remove_links'))

            _index += 1
