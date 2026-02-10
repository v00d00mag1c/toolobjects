from App.Objects.Act import Act
from App.Objects.Object import Object
from App.Objects.Arguments.ArgumentDict import ArgumentDict
from App.Objects.Arguments.Argument import Argument
from App.Objects.Arguments.Assertions.NotNone import NotNone

class Convert(Act):
    @classmethod
    def _arguments(cls) -> ArgumentDict:
        return ArgumentDict(items = [
            Argument(
                name = 'from',
                by_id = True,
                orig = Object,
                assertions = [NotNone()]
            ),
            Argument(
                name = 'to',
                orig = Object,
                assertions = [NotNone()]
            )
        ])

    async def implementation(self, i):
        _variant = 0
        _from = i.get('from')
        _to = i.get('to')
        _converts = _from.findConvertationsForClass(_to)
        if len(_converts) == 0:
            return None

        _convert = _converts[_variant]
        return await _convert.item().execute({
            'orig': _from
        })
