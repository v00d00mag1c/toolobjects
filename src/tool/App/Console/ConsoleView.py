from App.Objects.Arguments.ArgumentDict import ArgumentDict
from App.Objects.Arguments.ArgumentValues import ArgumentValues
from App.Objects.Arguments.Argument import Argument
from App.Objects.Executable import Executable
from App.Objects.Responses.ObjectsList import ObjectsList
from App.Objects.Responses.NoneResponse import NoneResponse
from Data.JSON import JSON
from Data.Boolean import Boolean
from Data.String import String
from App.Objects.View import View
from App import app

class ConsoleView(View):
    '''
    View that represents CMD
    '''

    async def byString(self, argv_str: str):
        _parsed_argv = app.app._parse_argv(argv_str.split(' '))

        return await self.execute(_parsed_argv[0])

    async def implementation(self, i: ArgumentValues = {}):
        self.log("Some arguments cannot be passed in console.")

        i.set('auth', self._auth(i.get('username'), i.get('password')))

        pre_i = i.get('pre_i')()
        results = await pre_i.execute(i)

        self._print_call(results, i.get('console_view.print_result'), i.get('console_view.print_as'))

    def _auth(self, username, password):
        return app.AuthLayer.login(
            name = username,
            password = password,
            login_from = 'console'
        )

    def _print_call(self, results, print_result: bool = True, print_as: bool = 'str'):
        if print_result == True:
            if results == None or results.isInstance(NoneResponse):
                self.log('nothing returned', role = ['empty_response', 'view_message'])
                return

            if print_as == 'str' and isinstance(results, ObjectsList):
                for item in results.getItems():
                    self.log_raw(item.displayAsString())
            else:
                self.log_raw(JSON(data = results.to_json()).dump(indent = 4))

    @classmethod
    def _arguments(cls) -> ArgumentDict:
        return ArgumentDict(items = [
            Argument(
                name = 'console_view.print_result',
                orig = Boolean,
                default = True
            ),
            Argument(
                name = 'console_view.print_as',
                orig = String,
                default = 'str'
            ),
            Argument(
                name = 'username',
                orig = String,
                default = 'root'
            ),
            Argument(
                name = 'password',
                orig = String,
                default = 'root'
            ),
        ],
            missing_args_inclusion = True
        )
