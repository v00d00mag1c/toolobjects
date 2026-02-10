from App.DB.Adapters.Connection.SQLAlchemyAdapter import SQLAlchemyAdapter
from pydantic import Field
from typing import Literal, Any

class SQLiteAdapter(SQLAlchemyAdapter):
    content: str = Field(default = None)

    def getContent(self, storage_di: Any = None):
        if self.content != None:
            return str(self.content)
        else:
            return str(storage_di.getDir().joinpath(storage_di.name + '.db'))

    def _constructor(self, storage_di: Any = None):
        protocol = 'sqlite'
        connection_string = protocol + self.delimiter + self.getContent(storage_di)

        self._get_engine(connection_string)
        self._init_models()

    def _get_engine(self, connection_string: str):
        from sqlalchemy import create_engine

        self._engine = create_engine(connection_string)
