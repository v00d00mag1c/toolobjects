from .Test import Test
from App.Queue.Run import Run
from App.Queue.Item import Item
from App.Arguments.ArgumentsDict import ArgumentsDict
from App.Arguments.Objects.List import List
from App.Arguments.Types.Int import Int

class QueueTest(Test):
    async def implementation(self, i):
        self.log('queue test')

        runs = Run()
        args = ArgumentsDict(items = {
            'prestart': '''
            [{
            "predicate": "App.Arguments.Types.Int", 
            "build": {"name": "random", "current": 0}
            }]
            ''',
            'items': '''
            [{
                "predicate": "Data.Random.Random",
                "arguments": {
                    "min": 0,
                    "max": 10000
                }
            },
            {
                "predicate": "App.Operations.Equate.Equate",
                "arguments": {
                    "link": {
                        "direct_value": "$0",
                    },
                    "to": {
                        "direct_value": "#0.data.0.content.number",
                    }
                }
            },
            {
                "predicate": "Web.URL.URL",
                "arguments": {
                    "db": "content",
                    "url": {
                        "value": "https://otvet.imgsmail.ru/download/21918917_b3d8927e6c78d2446cb2b924c1a5815f_800.jpg?r=x",
                        "replacements": [{
                            "position": (87, 88),
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
            }]
            '''
        })
        return await runs.execute(args)
