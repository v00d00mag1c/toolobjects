from App.Objects.Object import Object
from App.Storage.StorageUUID import StorageUUID
from App.Objects.Arguments.ListArgument import ListArgument
from App.Daemons.Daemon.Daemon import Daemon
from pydantic import Field
from App import app

class List(Object):
    items: list[Daemon] = Field(default = [])

    @classmethod
    def mount(cls):
        daemons = cls(
            items = []
        )

        for item in cls.getOption('daemons.autostart'):
            daemons.add(item.toPython())

        app.mount('DaemonList', daemons)

    def run_autostart(self):
        pass

    def add(self, item: Daemon):
        self.items.append(item)

    def remove(self, item: Daemon):
        if item in self.items:
            self.items.remove(item)

    @classmethod
    def _settings(cls):
        return [
            ListArgument(
                name = 'daemons.autostart',
                default = [],
                orig = Daemon,
            )
        ]
