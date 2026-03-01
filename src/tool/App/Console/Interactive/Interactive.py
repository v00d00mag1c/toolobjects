from App.Console.Console import Console
from App.Objects.Responses.NoneResponse import NoneResponse
from App.Objects.Arguments.ArgumentValues import ArgumentValues
from App.Objects.Object import Object
from App import app
import traceback

class Interactive(Console):
    _history: list[str] = []
    _pre_i: Object = None

    async def _implementation(self, i):
        from colorama import init

        init()

        self._auth(i)

        self.pre_i = i.get('pre_i')()

        is_exit = False

        self.log("pass values (-i App.Console.Interactive.Exit or Ctrl+C to exit)")

        while is_exit != True:
            _args_input = input("")
            _args = None

            try:
                _parsed_argv = app.app._parse_argv(_args_input.split(' '))
                _args = _parsed_argv[0]
                _args['auth'] = i.get('auth')
                self._history.append(_args)

                results = await self.pre_i.execute(_args)
                self._print_call(results, i)
            except Exception as e:
                self.log_error(e)

            self.log_raw('\n-------\n')

        return NoneResponse()
