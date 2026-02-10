from App.Objects.Act import Act
from App.Objects.Arguments.ArgumentDict import ArgumentDict
from App.Objects.Arguments.Argument import Argument
from App.Objects.Arguments.Assertions.NotNone import NotNone
from App.Objects.Responses.ObjectsList import ObjectsList
from Data.Types.String import String
from App import app

class Get(Act):
    @classmethod
    def _arguments(cls) -> ArgumentDict:
        return ArgumentDict(items = [
            Argument(
                name = 'name',
                orig = String,
                assertions = [NotNone()]
            )
        ])

    def _implementation(self, i):
        return ObjectsList(items = [app.Storage.get(i.get('name'))], unsaveable = True)
