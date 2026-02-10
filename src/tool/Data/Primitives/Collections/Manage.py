from App.Objects.Act import Act
from App.Objects.Arguments.ArgumentDict import ArgumentDict
from App.Objects.Arguments.Argument import Argument
from App.Objects.Arguments.ListArgument import ListArgument
from App.Objects.Arguments.LiteralArgument import LiteralArgument
from App.Objects.Arguments.Assertions.NotNone import NotNone
from Data.Primitives.Collections.Collection import Collection
from App.Objects.Object import Object
from Data.String import String

class Manage(Act):
    @classmethod
    def _arguments(cls) -> ArgumentDict:
        return ArgumentDict(items = [
            Argument(
                name = 'collection',
                by_id = True,
                orig = Collection,
                assertions = [NotNone()]
            ),
            ListArgument(
                name = 'items',
                orig = Object,
                by_id = True,
                assertions = [NotNone()]
            ),
            LiteralArgument(
                name = 'act',
                values = ['add', 'remove'],
                strict = True,
                default = 'add',
                orig = String
            )
        ])

    def implementation(self, i):
        collection = i.get('collection')
        items = i.get('items')
        act = i.get('act')

        for item in items:
            _ids = [item.getDbIds(), collection.getDbIds()]
            _roles = ['common', 'list_item']

            if act == 'add':
                collection.link(item, _roles)

                self.log_success('linked item {0} to collection {1}'.format(*_ids))
            else:
                collection.unlink(item, _roles)

                self.log_success('unlinked item {0} from collection {1}'.format(*_ids))
