from App.Objects.Act import Act
from App.Objects.Object import Object
from App.Objects.Arguments.ArgumentDict import ArgumentDict
from App.Objects.Arguments.Argument import Argument
from App.Objects.Arguments.Assertions.NotNoneAssertion import NotNoneAssertion
from Data.String import String

class Navigate(Act):
    @classmethod
    def _arguments(cls) -> ArgumentDict:
        return ArgumentDict(items = [
            Argument(
                name = 'with',
                orig = Object,
                default = 'Media.Files.Explorer', # App.Storage.VirtualPath.Navigate
                assertions = [NotNoneAssertion()]
            ),
            Argument(
                name = 'path',
                orig = String
            )
        ],
        missing_args_inclusion = True)

    async def implementation(self, i):
        _item = i.get('with')

        assert hasattr(_item, 'protocol_name'), "class is not a protocol"

        _obj = _item()
        #if i.get('path') != None:
        return await _obj.execute(i)
