from App.Objects.Act import Act
from App.Objects.Arguments.ArgumentDict import ArgumentDict
from App.Objects.Arguments.Argument import Argument
from App.Objects.Queue.Queue import Queue
from App.ACL.User import User

class Run(Act):
    @classmethod
    def _arguments(cls) -> ArgumentDict:
        return ArgumentDict(items=[
            Argument(
                name = 'queue',
                by_id = True,
                orig = Queue
            ),
            Argument(
                name = 'auth',
                orig = User
            )
        ])

    async def _implementation(self, i):
        return await i.get('queue').run(i.get('auth'))
