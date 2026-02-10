from App.Objects.Test import Test
from App.Tests.ConsoleLogTest import ConsoleLogTest
from App.Daemons.Daemon import Daemon
from App import app

class DaemonTest(Test):
    async def implementation(self, i):
        runs = ConsoleLogTest()
        runs.args = {}
        _storage = app.Storage.get('content')
        _item = _storage.adapter.flush(runs)

        _object = _item.getObject()
        daemon = Daemon(
            item = _object,
            max_iterations = 100
        )
        await daemon.start()
        print(daemon.getModule())
