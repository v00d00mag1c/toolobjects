from App.Tests.Test import Test
from App.Console.PrintLog import PrintLog

class ConsoleLogTest(Test):
    async def implementation(self, i):
        prints = PrintLog()
        await prints.execute(i = {
            'log': {
                'message': '55555555555',
                'time': -1,
                'section': {'value': ['TestSection']},
                'kind': {'value': 'bright'},
                'prefix': {'id': 7777777777777777777777777777, 'name': 'PREFIX'} 
            }
        })
