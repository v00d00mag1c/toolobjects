from App.Objects.Test import Test
from App.Objects.Queue.Run import Run
from App.Objects.Queue.Queue import Queue
from App.Objects.Arguments.ArgumentDict import ArgumentDict

class ValueReplace(Test):
    @classmethod
    def _arguments(cls) -> ArgumentDict:
        return ArgumentDict(missing_args_inclusion=True)

    async def _implementation(self, i):
        self.log('queue test')

        queue = Queue(
            prestart = [{
                'predicate': 'Data.Types.Int',
                'build': {
                    'name': 'random',
                    'current': 0
                }
            }],
            items = [
                {
                    'predicate': 'Data.Random.GetRandomInt',
                    'arguments': {
                        'min': 0,
                        'max': 62
                    }
                },
                {
                    'predicate': 'App.Objects.Queue.Operations.Equate',
                    'arguments': {
                        'equate_this': {
                            'direct_value': '$0'
                        },
                        'to': {
                            'direct_value': '#0'
                        }
                    }
                },
                {
                    'predicate': 'App.Storage.Movement.Save',
                    'arguments': {
                        'storage': ['tmp'],
                        'items': {
                            'direct_value': '#0'
                        }
                    }
                },
                {
                    'predicate': 'Web.URL',
                    'build': {
                        'value': {
                            'value': 'https://i.ibb.co/rG42gtzg/image.png?v=',
                            'replacements': [{
                                'position': (38, 39),
                                'value': '#0.items.0.value'
                            }]
                        }
                    },
                    'arguments': {
                        'force_flush': True
                    }
                }
            ],
            output = [
                {
                    'value': '#3.items'
                }
            ],
            return_index = 0
        )

        return await Run().execute({
            'queue': queue,
            'auth': i.get('auth')
        })
