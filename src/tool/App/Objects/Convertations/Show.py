from App.Objects.Act import Act
from App.Objects.Object import Object
from App.Objects.Arguments.ArgumentDict import ArgumentDict
from App.Objects.Arguments.Argument import Argument
from App.Objects.Arguments.Assertions.NotNoneAssertion import NotNoneAssertion
from App.Objects.Responses.ObjectsList import ObjectsList

class Show(Act):
    @classmethod
    def _arguments(cls) -> ArgumentDict:
        return ArgumentDict(items = [
            Argument(
                name = 'from',
                id_allow = True,
                orig = Object,
                assertions = [NotNoneAssertion()]
            )
        ])

    async def implementation(self, i):
        _list = ObjectsList()
        for submodule in i.get('from').getSubmodules(with_role=['convertation']):
            _list.append(submodule)

        return _list
