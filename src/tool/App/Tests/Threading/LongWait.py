from App.Objects.Test import Test
from App.Objects.Arguments.ArgumentDict import ArgumentDict
from App.Objects.Arguments.Argument import Argument
from Data.Float import Float
import asyncio

class LongWait(Test):
    @classmethod
    def _arguments(cls) -> ArgumentDict:
        return ArgumentDict(
            items = [
                Argument(
                    name = 'time',
                    orig = Float,
                    default = 50
                )
            ]
        )

    async def implementation(self, i):
        self.log('sleeping')

        await asyncio.sleep(i.get('time'))

        self.log_success('sleeped for {0}'.format(i.get('time')))
