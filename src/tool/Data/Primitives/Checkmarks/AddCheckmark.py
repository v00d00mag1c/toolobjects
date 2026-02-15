from App.Objects.Act import Act
from App.Objects.Arguments.Argument import Argument
from App.Objects.Arguments.ArgumentDict import ArgumentDict
from App.Objects.Arguments.Assertions.NotNone import NotNone
from App.Objects.Responses.ObjectsList import ObjectsList
from Data.Primitives.Checkmarks.Checkmark import Checkmark
from Data.Primitives.Checkmarks.List import List
from Data.Types.String import String
from Data.Types.Boolean import Boolean

class AddCheckmark(Act):
    @classmethod
    def _arguments(cls) -> ArgumentDict:
        return ArgumentDict(items = [
            Argument(
                name = 'list',
                by_id = True,
                orig = List
            ),
            Argument(
                name = 'save_to_list',
                orig = Boolean,
                default = True
            ),
            Argument(
                name = 'label',
                assertions = [NotNone()],
                default = '',
                # literally = True,
                orig = String
            )
        ])

    def _implementation(self, i):
        _label = i.get('label')
        checkmarks = i.get('list')

        checkmark = Checkmark()
        checkmark.label = _label
        checkmark.local_obj.make_public()
        checkmarks.link(checkmark)

        if i.get('save_to_list'):
            checkmarks.save()
            checkmark.save()

        return ObjectsList(items = [checkmark])
