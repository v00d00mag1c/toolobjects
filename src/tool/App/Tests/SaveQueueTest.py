from App.Objects.Test import Test
from Data.Random.GetRandomInt import GetRandomInt
from App.Queue.Run import Run
from App.Storage.Movement.Save import Save

class SaveQueueTest(Test):
    async def implementation(self, i):
        '''
        runs = Run()
        args = {
            'items': [
                {
                    'predicate': 'Data.Random.GetRandomInt',
                    'arguments': {
                        'min': 999,
                        'max': 8888888
                    }
                },
                {
                    "predicate": "App.Storage.Save.Save",
                    "arguments": {
                        "equate_this": {
                            "direct_value": "$0"
                        },
                    }
                }
            ]
        }'''

        rnd = GetRandomInt()
        val = await rnd.execute({'min': 99, 'max': 8888})
        _sav = Save()

        self.log_raw(await _sav.execute({
            'storage': 'tmp',
            'items': val
        }))
