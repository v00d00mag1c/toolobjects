from App.Objects.Object import Object
from pydantic import Field
from typing import Optional
import datetime

class Entry(Object):
    title: str = Field(default = None)
    description: str = Field(default = None)
    guid: Optional[str] = Field(default = None)

    def set_pubdate(self, date: datetime.datetime):
        self.obj.declared_created_at = date
