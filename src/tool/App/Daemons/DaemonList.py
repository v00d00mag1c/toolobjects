from App.Objects.Object import Object
from App.Daemons.DaemonItem import DaemonItem
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

        for item in cls.get('daemons.autostart'):
            daemons.append(item)

        app.mount('Daemons', daemons)

    @classmethod
    def getSettings(cls):
        from App.Arguments.Objects.List import List

        return [
            List(
                name = 'daemons.autostart',
                orig = Daemon
            )
        ]
