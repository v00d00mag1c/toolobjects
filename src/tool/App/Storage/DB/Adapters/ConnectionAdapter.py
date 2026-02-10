from App.Objects.Object import Object
from pydantic import Field
from typing import Any, ClassVar

class ConnectionAdapter(Object):
    protocol_name: ClassVar[str] = ''

    protocol: str = Field(default = 'none')
    delimiter: str = Field(default = ':///')

    ObjectAdapter: Any = None
    ObjectLinkAdapter: Any = None

    def flush(self, item: Object):
        pass
