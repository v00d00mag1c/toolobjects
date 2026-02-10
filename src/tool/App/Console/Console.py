from App.Objects.Arguments.ArgumentDict import ArgumentDict
from App.Objects.Arguments.ArgumentValues import ArgumentValues
from App.Objects.Arguments.Argument import Argument
from App.Objects.Arguments.AllowedValues import AllowedValues
from App.Objects.Executable import Executable
from App.Objects.Responses.ObjectsList import ObjectsList
from App.Objects.Responses.NoneResponse import NoneResponse
from App.Objects.Threads.ExecutionThread import ExecutionThread
from Data.Types.JSON import JSON
from Data.Types.Boolean import Boolean
from Data.Types.String import String
from App.Objects.View import View
from App import app

class Console(View):
    '''
    View that represents CMD
    '''

    async def byString(self, argv_str: str):
        _parsed_argv = app.app._parse_argv(argv_str.split(' '))

        return await self.execute(_parsed_argv[0])

    async def _implementation(self, i: ArgumentValues = {}):
        self.log("Some arguments cannot be passed in console.")

        self._auth(i)
        pre_i = i.get('pre_i')()

        thread = ExecutionThread(id = 0)
        thread.set(pre_i.execute(i))
        results = await thread.get()
        thread.end()
        #results = await pre_i.execute(i)

        self._print_call(results, i)

    def _print_call(self, results, i):
        if i.get('console.print') == True:
            if results == None or results.isInstance(NoneResponse):
                self.log('nothing returned', role = ['console.print.returned.nothing', 'view.message'])
                return

            if i.get('console.print.as') == 'str' and isinstance(results, ObjectsList):
                _displays = list()
                for item in results.getItems():
                    if hasattr(item, 'displayAsString') == False:
                        self.log_raw('[item without displayAsString]')
                        continue

                    _displays.append(item.displayAsString(show_id = i.get('console.print.display_ids')))

                self.log_raw(i.get('console.print.divider').join(_displays))
            else:
                self.log_raw(JSON(data = results.to_json(exclude_none = True, exclude_defaults = True)).dump(indent = 4))

    def _auth(self, i):
        if i.get('auth') != None:
            i.set('auth', app.AuthLayer.byToken(i.get('auth')))
        else:
            i.set('auth', app.AuthLayer.getUserByName('root'))

    @classmethod
    def canBeUsedBy(self, user):
        return False

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
                default = 'str',
                allowed_values = AllowedValues(
                    values = ['str', 'json'],
                    strict = True
                )
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
                name = 'auth',
                # orig = String, do not comparing
                default = None
            )
        ],
            missing_args_inclusion = True
        )
