from App.Objects.Act import Act
from App.Objects.Arguments.ArgumentDict import ArgumentDict
from App.Objects.Arguments.Argument import Argument
from App.Objects.Arguments.ListArgument import ListArgument
from App.Objects.Arguments.Assertions.NotNoneAssertion import NotNoneAssertion
from App.Objects.Responses.ObjectsList import ObjectsList
from Data.String import String
from App import app

class Get(Act):
    @classmethod
    def _arguments(cls) -> ArgumentDict:
        return ArgumentDict(items = [
            ListArgument(
                name = 'key',
                orig = String,
                assertions = [NotNoneAssertion()]
            )
        ])

    def implementation(self, i):
        _list = ObjectsList(items = [], unsaveable = True)

        for key in i.get('key'):
            _key = app.Locales.get(key)
            if _key != None:
                _list.append(_key)

        return _list
