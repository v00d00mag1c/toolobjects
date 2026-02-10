from App.Console.ConsoleView import ConsoleView
from App.Responses.NoneResponse import NoneResponse
from App.Arguments.ArgumentValues import ArgumentValues
from App import app
import traceback

class InteractiveView(ConsoleView):
    async def implementation(self, i):
        pre_i = i.get('pre_i')()

        is_exit = False
        prev = None
    
        self.log("pass arguments (-i App.Console.Exit to exit)")

        while is_exit != True:
            _args_input = input("")
            _parsed_argv = app.app._parse_argv(_args_input.split(' '))
            _args = _parsed_argv[0]
            _i = _args.get('i')
            if _i == 'App.Console.Exit':
                is_exit = True
                break
            if _i == 'App.Console.Same':
                _args['i'] = prev

            try:
                results = await pre_i.execute(_args)
                self._print_call(results, i.get('console_view.print_result'), i.get('console_view.print_as'))
            except Exception as e:
                traceback.print_exc()

            prev = _i
            self.log_raw('\n-------\n')

        return NoneResponse()
