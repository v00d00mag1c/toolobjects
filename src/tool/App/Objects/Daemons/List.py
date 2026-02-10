from App.Objects.Object import Object
from App.Storage.StorageUUID import StorageUUID
from App.Objects.Arguments.ListArgument import ListArgument
from App.Objects.Daemons.DaemonItem import DaemonItem
from pydantic import Field
from App import app

class List(Object):
    items: list[DaemonItem] = Field(default = [])

    @classmethod
    def mount(cls):
        daemons = cls(
            items = []
        )

        for item in cls.getOption('daemons.autostart'):
            daemons.items.append(item.toPython())

        app.mount('DaemonList', daemons)

    @classmethod
    def _settings(cls):
        return [
            ListArgument(
                name = 'daemons.autostart',
                default = [],
                orig = DaemonItem,
            )
        ]
