from App.Objects.Act import Act
from App.Objects.Arguments.ArgumentDict import ArgumentDict
from App.Objects.Arguments.Argument import Argument
from Data.Int import Int
from Data.Boolean import Boolean
from App.Storage.StorageItem import StorageItem
from App.Objects.Arguments.Assertions.NotNoneAssertion import NotNoneAssertion
from App.Responses.ObjectsList import ObjectsList

class ExecuteById(Act):
    @classmethod
    def getArguments(cls) -> ArgumentDict:
        return ArgumentDict(items = [
            Argument(
                name = 'storage',
                orig = StorageItem,
                assertions = [NotNoneAssertion()]
            ),
            Argument(
                name = 'uuid',
                orig = Int,
                assertions = [NotNoneAssertion()]
            ),
            Argument(
                name = 'link',
                default = True,
                orig = Boolean
            ),
            Argument(
                name = 'sift',
                default = True,
                orig = Boolean
            )
        ])

    async def implementation(self, i):
        _storage = i.get('storage')
        obj = _storage.adapter.ObjectAdapter.getById(i.get('uuid'))

        assert obj != None, 'object with this uuid not found'

        _old = obj.toPython()
        _exec = obj.toPython()
        _args = _exec.args.copy()
        _args.update(i.getValues(exclude = ['storage', 'uuid', 'link', 'sift']))

        assert _exec != None, 'not found object'
        assert _exec.canBeExecuted(), 'object does not contains execute interface'

        _res = await _exec.execute(i = _args)

        if i.get('sift') == True:
            _res = await _exec.update(_old, _res)

        obj.flush_content(_exec)
        if isinstance(_res, ObjectsList):
            if i.get('link') == True:
                for item in _res.getItems():
                    _exec.link(item)

        return _res
