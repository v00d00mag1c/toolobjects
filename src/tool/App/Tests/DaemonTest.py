from App.Objects.Test import Test
from App.Tests.ConsoleLogTest import ConsoleLogTest
from App.Daemons.Daemon import Daemon
from App import app

class DaemonTest(Test):
    async def implementation(self, i):
        daemon = Daemon(
            item = ConsoleLogTest(),
            max_iterations = 100
        )
        await daemon.start()
        self.log_raw(daemon.getModule())
