from App.Objects.Object import Object
from App.Daemons.DaemonItem import DaemonItem
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

        app.mount('Daemons', daemons)

    @classmethod
    def getSettings(cls):
        return [
            ListArgument(
                name = 'daemons.autostart',
                default = [],
                orig = DaemonItem,
            )
        ]
