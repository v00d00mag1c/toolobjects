from App.Objects.Test import Test
from App.Queue.Run import Run

class QueueTest(Test):
    async def implementation(self, i):
        self.log('queue test')

        runs = Run()
        args = {
            'prestart': '''
            [{
            "predicate": "Data.Int", 
            "build": {"name": "random", "current": 0}
            }]
            ''',
            'items': '''
            [{
                "predicate": "Data.Random.GetRandomInt.GetRandomInt",
                "arguments": {
                    "min": 0,
                    "max": 10000
                }
            },
            {
                "predicate": "App.Queue.Operations.Equate",
                "arguments": {
                    "equate_this": {
                        "direct_value": "$0"
                    },
                    "to": {
                        "direct_value": "#0.items.0.value"
                    }
                }
            }]''',
            'output': '''
            [{
                "key": "#0",
                "response": "App.Objects.Responses.AnyResponse"
            }]
            '''
        }
        '''
            {
                "predicate": "App.DB.Save",
                "arguments": {
                    "object": {
                        "direct_value": "#1"
                    }
                }
            }
            {
                "name": "Web.URL",
                "arguments": {
                    "url": {
                        "value": "",
                        "replacements": [{
                            "position": (36, 37),
                            "value": "#0.current"
                        }
                }
            }
                    {
                "predicate": "Web.URL",
                "arguments": {
                    "db": "content",
                    "url": {
                        "value": "https://otvet.imgsmail.ru/download/21918917_b3d8927e6c78d2446cb2b924c1a5815f_800.jpg?r=x",
                        "replacements": [{
                            "position": [87, 88],
                            "value": "#0.current"
                        }]
                    }
                }
            },
            {
                "predicate": "Web.URL.Download",
                "arguments": {
                    "db": "content",
                    "url": {
                        "direct_value": "$2.data.0"
                    }
                }
            }
        '''
        return await runs.execute(args)
