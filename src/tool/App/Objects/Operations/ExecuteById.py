from App.Objects.Act import Act
from App.Objects.Arguments.ArgumentDict import ArgumentDict
from App.Objects.Arguments.Argument import Argument
from Data.Int import Int
from Data.Boolean import Boolean
from App.Storage.StorageItem import StorageItem
from App.Storage.StorageUUID import StorageUUID
from App.Objects.Arguments.Assertions.NotNoneAssertion import NotNoneAssertion
from App.Objects.Responses.ObjectsList import ObjectsList

class ExecuteById(Act):
    @classmethod
    def getArguments(cls) -> ArgumentDict:
        return ArgumentDict(items = [
            Argument(
                name = 'item',
                orig = StorageUUID,
                assertions = [NotNoneAssertion()]
            ),
            Argument(
                name = 'link',
                default = True,
                orig = Boolean
            ),
            Argument(
                name = 'is_update',
                default = True,
                orig = Boolean
            )
        ])

    async def implementation(self, i):
        _obj = i.get('item')
        obj = _obj.getItem()

        assert obj != None, 'object with this uuid not found'

        _old = obj.toPython()
        _exec = obj.toPython()
        _args = _exec.args.copy()
        _args.update(i.getValues(exclude = ['storage', 'uuid', 'link', 'is_update']))

        assert _exec != None, 'not found object'
        assert _exec.canBeExecuted(), 'object does not contains execution interface'

        _res = await _exec.execute(i = _args)

        if i.get('is_update') == True:
            _res = await _exec.update(_old, _res)

        obj.flush_content(_exec)
        if isinstance(_res, ObjectsList):
            if i.get('link') == True:
                for item in _res.getItems():
                    _exec.link(item)

        return _res
