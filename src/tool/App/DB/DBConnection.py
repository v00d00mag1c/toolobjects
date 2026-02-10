from App.Objects.Object import Object
from App.DB.SQLiteConnection import SQLiteConnection
from pydantic import Field
from typing import Literal, Any
from enum import Enum
from App import app

class DBConnection(Object):
    protocol: Literal['sqlite'] = Field()
    content: str | dict = Field(default = None)
    connection: Any = None
    _storageitem: Any = None

    def getContent(self):
        if self.content != None:
            return self.content
        else:
            return str(self._storageitem.getDir().joinpath(self._storageitem.name + '.db'))

    def _constructor(self, storageitem_di):
        self._storageitem = storageitem_di

        match (self.protocol):
            # Todo move to enum
            case 'sqlite':
                self.connection = SQLiteConnection(content = self.getContent())
