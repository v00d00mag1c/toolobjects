from App.Objects.Test import Test
from App.Objects.Object import Object
from App.Tests.ConsoleLogTest import ConsoleLogTest
from App.Objects.Arguments.ArgumentDict import ArgumentDict
from App.Objects.Arguments.Argument import Argument
from App.Objects.Arguments.Assertions.NotNoneAssertion import NotNoneAssertion
from App.Daemons.Daemon.Daemon import Daemon
from Data.Int import Int
from Data.Float import Float
from App import app

class RunScript(Test):
    @classmethod
    def _arguments(cls) -> ArgumentDict:
        return ArgumentDict(items = [
            Argument(
                name = 'i_daemon',
                orig = Object,
                assertions = [NotNoneAssertion()]
            ),
            Argument(
                name = 'interval',
                orig = Float,
                default = 10
            ),
            Argument(
                name = 'max_iterations',
                orig = Int,
                default = -1
            )
        ])

    async def implementation(self, i):
        _object = i.get('i_daemon')

        assert _object != None

        _args = i.getValues(exclude = ['i_daemon', 'interval', 'max_iterations']).copy()

        daemon_item = _object()
        
        assert daemon_item.canBeExecuted(), 'non-executable'

        daemon_item.args = _args
        daemon = Daemon(
            item = daemon_item,
            interval = i.get('interval'),
            max_iterations = i.get('max_iterations'),
        )

        await daemon.start()
