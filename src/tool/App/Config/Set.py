from App.Objects.Act import Act
from App.Objects.Arguments.ArgumentDict import ArgumentDict
from App.Objects.Arguments.Argument import Argument
from App.Objects.Arguments.Assertions.NotNone import NotNone
from App.Objects.Responses.AnyResponse import AnyResponse
from Data.Types.Any import Any
from Data.Types.String import String
from Data.Types.Boolean import Boolean
from App import app

class Set(Act):
    @classmethod
    def _arguments(cls) -> ArgumentDict:
        return ArgumentDict(items = [
            Argument(
                name = 'key',
                orig = String,
                assertions = [NotNone()]
            ),
            Argument(
                name = 'value',
                orig = Any,
                assertions = [NotNone()]
            ),
            Argument(
                name = 'save_previous',
                orig = Boolean,
                default = True
            )
        ])

    def _implementation(self, i):
        key = i.get('key')
        val = i.get('value')

        app.Config.getItem().set(key, val, i.get('save_previous'))
