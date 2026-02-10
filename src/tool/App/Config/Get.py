from App.Objects.Act import Act
from App.Objects.Arguments.ArgumentDict import ArgumentDict
from App.Objects.Arguments.ListArgument import ListArgument
from App.Objects.Arguments.Assertions.NotNone import NotNone
from App.Objects.Responses.AnyResponse import AnyResponse
from Data.String import String
from App import app

class Get(Act):
    @classmethod
    def _arguments(cls) -> ArgumentDict:
        return ArgumentDict(items = [
            ListArgument(
                name = 'key',
                orig = String,
                assertions = [NotNone()]
            )
        ])

    def _implementation(self, i):
        _vals = dict()
        for key in i.get('key'):
            _vals[key] = app.Config.get(key)

        return AnyResponse(data = _vals)
