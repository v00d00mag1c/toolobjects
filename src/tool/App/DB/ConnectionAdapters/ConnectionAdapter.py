from App.Objects.Object import Object
from pydantic import Field
from typing import Any

class ConnectionAdapter(Object):
    protocol: str = Field(default = 'none')
    delimiter: str = Field(default = ':///')

    ObjectAdapter: Any = None
    ObjectLinkAdapter: Any = None

    def insertObject(self, item: Object):
        pass
