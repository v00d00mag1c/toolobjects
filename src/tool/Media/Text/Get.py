from App.Objects.Extractor import Extractor
from App.Objects.Object import Object
from App.Objects.Arguments.ArgumentDict import ArgumentDict
from App.Objects.Arguments.Argument import Argument
from App.Objects.Arguments.Assertions.NotNone import NotNone
from Data.Types.String import String
from Media.Text.Text import Text

class Get(Extractor):
    @classmethod
    def _arguments(cls) -> ArgumentDict:
        return ArgumentDict(items = [
            Argument(
                name = 'object',
                orig = Object,
                assertions = [NotNone()]
            ),
            Argument(
                name = 'text',
                orig = String,
                assertions = [NotNone()]
            )
        ])

    def _implementation(self, i):
        self.append(i.get('object')(
            value = i.get('text')
        ))
