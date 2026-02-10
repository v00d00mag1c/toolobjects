from typing import Any

class DBInsertable():
    _db: Any = None  # : ConnectionAdapterObject

    def setDb(self, db):
        self._db = db

    def getDbId(self):
        return self._db.uuid
