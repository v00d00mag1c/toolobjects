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

        i.set('auth', self._auth(i.get('auth_username'), i.get('auth_password')))

        pre_i = i.get('pre_i')()
        results = await pre_i.execute(i)

        self._print_call(results, i)

    def _auth(self, username, password):
        return app.AuthLayer.login(
            name = username,
            password = password,
            login_from = 'console'
        )

    def _print_call(self, results, i):
        if i.get('console.print') == True:
            if results == None or results.isInstance(NoneResponse):
                self.log('nothing returned', role = ['empty_response', 'view_message'])
                return

            if i.get('console.print.as') == 'str' and isinstance(results, ObjectsList):
                _displays = list()
                for item in results.getItems():
                    if hasattr(item, 'displayAsString') == False:
                        self.log_raw('[item without displayment]')
                        continue

                    _displays.append(item.displayAsString(show_id = i.get('console.print.display_ids')))

                self.log_raw(i.get('console.print.divider').join(_displays))
            else:
                self.log_raw(JSON(data = results.to_json()).dump(indent = 4))

    @classmethod
    def _arguments(cls) -> ArgumentDict:
        return ArgumentDict(items = [
            Argument(
                name = 'console.print',
                orig = Boolean,
                default = True
            ),
            Argument(
                name = 'console.print.as',
                orig = String,
                default = 'str'
            ),
            Argument(
                name = 'console.print.display_ids',
                orig = Boolean,
                default = True
            ),
            Argument(
                name = 'console.print.divider',
                orig = String,
                default = '\n'
            ),
            Argument(
                name = 'auth_username',
                orig = String,
                default = 'root'
            ),
            Argument(
                name = 'auth_password',
                orig = String,
                default = 'root'
            ),
        ],
            missing_args_inclusion = True
        )
