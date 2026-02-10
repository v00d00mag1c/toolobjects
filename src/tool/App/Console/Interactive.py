from App.Objects.Executable import Executable
from App.Responses.NoneResponse import NoneResponse
from App import app
import traceback

class Interactive(Executable):
    async def implementation(self, i):
        is_exits = False
        while is_exits != True:
            self.log('Pass the Object name')

            val = input("")
            if val == 'exit':
                is_exits = True
                break

            self.log('OK')
            self.log('Pass args (like --arg1 val1 --arg2 val2)')

            _args = input("")
            parsed = app.app._parse_argv(['cli.py'] + _args.split(' '))

            _executable = app.app.objects.getByName(val)
            executable = _executable.module()

            try:
                print(await executable.execute(parsed))
            except Exception as e:
                traceback.print_exc()

            print('-------')

        return NoneResponse()
