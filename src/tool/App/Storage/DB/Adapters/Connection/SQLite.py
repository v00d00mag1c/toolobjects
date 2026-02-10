from App.Storage.DB.Adapters.Connection.SQLAlchemy import SQLAlchemy
from App.Storage.DB.Adapters.Search.Condition import Condition
from pydantic import Field

class SQLite(SQLAlchemy):
    protocol_name = 'sqlite'
    content: str = Field(default = None)

    class QueryAdapter(SQLAlchemy.QueryAdapter):
        def _getComparement(self, condition: Condition):
            from sqlalchemy import func

            if condition.json_fields != None:
                return func.json_extract(getattr(self._model, condition.getFirst()), condition.json_fields)

            return getattr(self._model, condition.getFirst())

    def getConnectionStringContent(self):
        if self.content != None:
            return str(self.content)
        else:
            return str(self._storage_item.getDir().joinpath(self.name + '.db'))
