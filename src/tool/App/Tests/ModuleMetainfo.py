from App.Objects.Test import Test
from App.Objects.Arguments.ArgumentDict import ArgumentDict
from App.Objects.Arguments.Argument import Argument
from Data.Boolean import Boolean
from Data.String import String
from Data.JSON import JSON
from App import app

class ModuleMetainfo(Test):
    @classmethod
    def _arguments(cls) -> ArgumentDict:
        return ArgumentDict(items=[
            Argument(
                name = '1',
                default = False,
                orig = Boolean
            ),
            Argument(
                name = '2',
                orig = String
            )
        ])

    async def implementation(self, i):
        if i.get('1') == False:
            self.log('♥')
            return

        _obj = app.ObjectsList.getByName(i.get('2'))
        _obj.getModule()
        self.log_raw(JSON(data=_obj.to_json()).dump(indent = 4))
