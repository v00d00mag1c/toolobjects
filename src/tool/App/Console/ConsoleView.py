from App.Arguments.ArgumentDict import ArgumentDict
from App.Arguments.ArgumentValues import ArgumentValues
from App.Arguments.Assertions.NotNoneAssertion import NotNoneAssertion
from App.Arguments.Assertions.InputNotInValues import InputNotInValues
from App.Arguments.Objects.Executable import Executable
from App.Arguments.Types.Boolean import Boolean
from App.Arguments.Types.String import String
from App.Responses.ObjectsList import ObjectsList
from Data.JSON import JSON
from App.Objects.View import View
from App import app

class ConsoleView(View):
    '''
    View that represents CMD. Runs executable from "i"
    '''

    async def implementation(self, i: ArgumentValues = {}):
        pre_i = i.get('pre_i')()
        results = await pre_i.execute(i)

        self._print_call(results, i.get('console_view.print_result'), i.get('console_view.print_as'))

    def _print_call(self, results, print_result: bool = True, print_as: bool = 'str'):
        if print_result == True:
            if results == None:
                self.log('nothing returned', role = ['empty_response', 'view_message'])
                return

            if print_as != 'json' and isinstance(results, ObjectsList):
                for item in results.getItems():
                    self.log_raw(item.displayAs(print_as))
            else:
                self.log_raw(JSON(data = results.to_json()).dump(indent = 4))

    @classmethod
    def getArguments(cls) -> ArgumentDict:
        dicts = ArgumentDict(items = [
            Executable(
                name = 'pre_i',
                default = 'App.Objects.Operations.DefaultExecutorWheel',
                assertions = [
                    NotNoneAssertion()
                ]
            ),
            Boolean(
                name = 'console_view.print_result',
                default = True
            ),
            String(
                name = 'console_view.print_as',
                default = 'str'
            )
        ],
            missing_args_inclusion = True
        )

        return dicts
