from App.Objects.Extractor import Extractor
from App.Objects.Arguments.ArgumentDict import ArgumentDict
from App.Objects.Arguments.Argument import Argument
from App.Objects.Arguments.Assertions.NotNone import NotNone
from Data.Types.String import String
from Data.Primitives.Checkmarks.List import List

class CreateList(Extractor):
    @classmethod
    def _arguments(cls) -> ArgumentDict:
        return ArgumentDict(
            items = [
                Argument(
                    name = 'name',
                    orig = String,
                    assertions = [NotNone()]
                )
            ]
        )

    def _implementation(self, i):
        _list = List()
        _list.obj.name = i.get('name')

        self.append(_list)
