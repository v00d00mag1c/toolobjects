from App.Objects.Act import Act
from App.Objects.Object import Object
from App.Objects.Arguments.ArgumentDict import ArgumentDict
from App.Objects.Arguments.Argument import Argument
from App.Objects.Arguments.ListArgument import ListArgument
from App.Objects.Arguments.Assertions.NotNoneAssertion import NotNoneAssertion
from Data.String import String
from Data.Boolean import Boolean

class Edit(Act):
    @classmethod
    def _arguments(cls) -> ArgumentDict:
        return ArgumentDict(items = [
            Argument(
                name = 'object',
                orig = Object,
                literally = True,
                id_allow = True,
                assertions = [NotNoneAssertion()]
            ),
            ListArgument(
                name = 'key',
                orig = String,
                assertions = [NotNoneAssertion()]
            ),
            Argument(
                name = 'val',
                orig = None,
                assertions = [NotNoneAssertion()]
            ),
            Argument(
                name = 'update',
                default = True,
                orig = Boolean,
                assertions = [NotNoneAssertion()]
            )
        ])

    async def implementation(self, i):
        _obj = i.get('object')
        _keys = i.get('key')
        _link = _obj
        _last = _keys[-1]

        for key in _keys:
            if _link == None:
                self.log('no property with name {0}'.format(key))
                break

            if key == _last:
                setattr(_link, key, i.get('val'))
            else:
                _link = getattr(_link, key, None)

        if i.get('update') == True:
            _obj.save()
