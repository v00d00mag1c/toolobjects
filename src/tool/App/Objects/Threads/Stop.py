from App.Objects.Act import Act
from App.Objects.Arguments.ArgumentDict import ArgumentDict
from App.Objects.Arguments.Argument import Argument
from App.Objects.Arguments.Assertions.NotNoneAssertion import NotNoneAssertion
from Data.Int import Int
from App import app

class Stop(Act):
    @classmethod
    def _arguments(cls) -> ArgumentDict:
        return ArgumentDict(items = [
            Argument(
                name = 'id',
                orig = Int,
                assertions = [NotNoneAssertion()]
            )
        ])

    def implementation(self, i):
        _id = i.get('id')
        _item = app.ThreadsList.getById(_id)

        assert _item != None, 'not found thread'

        _item.end()
