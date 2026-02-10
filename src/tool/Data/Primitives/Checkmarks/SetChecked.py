from App.Objects.Act import Act
from App.Objects.Arguments.Argument import Argument
from App.Objects.Arguments.ArgumentDict import ArgumentDict
from App.Objects.Responses.ObjectsList import ObjectsList
from Data.Primitives.Checkmarks.Checkmark import Checkmark
from Data.Boolean import Boolean

class SetChecked(Act):
    @classmethod
    def _arguments(cls) -> ArgumentDict:
        return ArgumentDict(items = [
            Argument(
                name = 'item',
                by_id = True,
                orig = Checkmark
            ),
            Argument(
                name = 'state',
                default = False,
                orig = Boolean
            )
        ])
    
    def implementation(self, i):
        item = i.get('item')
        item.state = i.get('state')
        item.save()

        return ObjectsList(items = [item])
