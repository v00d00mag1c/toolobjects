from App.Storage.DB.Adapters.Connection.SQLAlchemyAdapter import SQLAlchemyAdapter
from pydantic import Field
from typing import Literal, Any

class SQLiteAdapter(SQLAlchemyAdapter):
    protocol_name = 'sqlite'
    content: str = Field(default = None)

    def getContent(self, storage_item: Any = None):
        if self.content != None:
            return str(self.content)
        else:
            return str(storage_item.getDir().joinpath(self.name + '.db'))

    def _constructor(self, storage_item: Any = None):
        protocol = 'sqlite'
        connection_string = protocol + self.delimiter + self.getContent(storage_item)

        self._get_engine(connection_string)
        self._init_models()

    def _get_engine(self, connection_string: str):
        from sqlalchemy import create_engine
        from sqlalchemy.orm import Session

        self._engine = create_engine(connection_string)
        self._session = Session(self._engine, expire_on_commit=False)
