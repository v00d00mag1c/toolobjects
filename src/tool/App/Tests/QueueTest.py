from .Test import Test

class QueueTest(Test):
    async def implementation(self, i):
        self.log('queue test')
