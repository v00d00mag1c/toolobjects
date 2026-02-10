from App.Objects.Object import Object
from pydantic import Field
from typing import Any
from App import app

class DaemonItem(Object):
    db: str = Field()
    uuid: int = Field()

    def getModule(self):
        _storage = app.Storage.get(self.db)
        _item = _storage.getAdapter().getById(self.uuid)

        return _item
