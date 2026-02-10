from typing import Any
from pydantic import computed_field

class DBInsertable():
    _db: Any = None  # : ConnectionAdapterObject

    def setDb(self, db):
        self._db = db

    def getDb(self):
        return self._db

    def getDbId(self):
        return self._db.uuid

    @computed_field
    @property
    def db_info(self) -> dict:
        if self.getDb() != None:
            return {
                'uuid': self.getDbId()
            }

        return None
