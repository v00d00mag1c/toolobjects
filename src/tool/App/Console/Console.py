from App.Arguments.ArgumentDict import ArgumentDict
from App.Arguments.Assertions.NotNoneAssertion import NotNoneAssertion
from App.Arguments.Assertions.InputNotInValues import InputNotInValues
from App.Arguments.Objects.Executable import Executable
from App.Arguments.Types.Boolean import Boolean
from Data.JSON import JSON
from App.View import View
from App import app

class Console(View):
    '''
    View that represents CMD. Runs executable from "i"
    '''

    async def implementation(self, i: dict = {}):
        executable = i.get('i')
        assert executable.canBeExecuted(), 'object does not contains execute interface'
        assert executable.canBeUsedBy(None), 'access denied'

        _item = executable()
        _item.integrate(i.values)
        results = await _item.execute(i = i)

        if i.get('print_result') == True:
            if results == None:
                self.log('nothing returned', role = ['empty_response', 'view_message'])
            else:
                self.log(f'{executable.getClassNameJoined()} returned:')
                self.log_raw(JSON(data = results.to_json()).dump(indent = 4))

    @classmethod
    def getArguments(cls) -> ArgumentDict:
        dicts = ArgumentDict(items = [
            Executable(
                name = 'i',
                default = 'App.Queue.Run.Run',
                assertions = [
                    NotNoneAssertion(),
                    InputNotInValues(values=['App.Console.Console.Console'])
                ]
            ),
            Boolean(
                name = 'print_result',
                default = True
            )
        ],
            missing_args_inclusion = True
        )

        return dicts
