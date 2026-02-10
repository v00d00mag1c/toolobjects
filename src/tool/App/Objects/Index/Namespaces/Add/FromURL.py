from App.Objects.Act import Act
from App.Objects.Arguments.ArgumentDict import ArgumentDict
from App.Objects.Arguments.Argument import Argument
from Data.String import String
from App.Objects.Index.Namespaces.Add.Add import Add

class FromURL(Act):
    @classmethod
    def _arguments(cls) -> ArgumentDict:
        return ArgumentDict(items = [
            Argument(
                name = 'url',
                orig = String,
                default = None
            )
        ],
        missing_args_inclusion = True)

    async def _implementation(self, i):
        assert False, 'not implemented'

        await Add().execute(i)
