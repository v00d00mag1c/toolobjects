from App.Objects.Object import Object
from App.Storage.StorageUUID import StorageUUID
from App.Objects.Arguments.ListArgument import ListArgument
from App.Daemons.Daemon import Daemon
from pydantic import Field
from App import app

class DaemonList(Object):
    items: list[Daemon] = Field(default = [])

    @classmethod
    def mount(cls):
        daemons = cls(
            items = []
        )

        for item in cls.getOption('daemons.autostart'):
            daemons.append(item)

        app.mount('DaemonList', daemons)

    def append(self, item):
        self.items.append(item.toPython())

    @classmethod
    def _settings(cls):
        return [
            ListArgument(
                name = 'daemons.autostart',
                default = [],
                orig = StorageUUID,
            )
        ]
