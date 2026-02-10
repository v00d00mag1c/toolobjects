from App.Objects.Act import Act
from App.Objects.Arguments.ArgumentDict import ArgumentDict
from App.Objects.Arguments.Argument import Argument
from App.Objects.Arguments.Assertions.NotNoneAssertion import NotNoneAssertion
from App.Objects.Responses.ObjectsList import ObjectsList
from Data.String import String
from Data.Boolean import Boolean
from App import app

class Get(Act):
    @classmethod
    def _arguments(cls) -> ArgumentDict:
        return ArgumentDict(items = [
            Argument(
                name = 'name',
                orig = String,
                assertions = [NotNoneAssertion()]
            ),
            Argument(
                name = 'load_module',
                orig = Boolean,
                default = False,
            )
        ])

    async def implementation(self, i):
        _items = ObjectsList(unsaveable = True, supposed_to_be_single = True)
        _obj = app.ObjectsList.getByName(i.get('name'))

        if i.get('load_module') == True:
            if _obj.hasModuleLoaded() == False:
                _obj.loadModuleLater()

        _items.append(_obj)

        return _items
