from App.Objects.Object import Object
from App.Daemons.DaemonItem import DaemonItem
from App.Objects.Arguments.Argument import Argument
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
            Argument(
                name = 'daemons.autostart',
                default = [],
                orig = DaemonItem,
                is_multiple = True
            )
        ]
