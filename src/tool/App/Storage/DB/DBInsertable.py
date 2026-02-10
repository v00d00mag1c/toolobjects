from typing import Any, Type
from pydantic import computed_field
from App.Storage.DB.DBInfo import DBInfo

class DBInsertable():
    _db: Any = None  # : ObjectAdapter

    def setDb(self, db):
        self._db = db

        # self.log(f"db was changed to {db._adapter._storage_item.name}, uuid is {db.uuid}")

    def getDb(self):
        '''
        Returns the adapted version of object
        '''

        '''if self.hasDb() == False:
            self.log("there is no db!")
        else:
            self.log(f"db is {self._db._adapter._storage_item.name}, sis!")
        '''

        return self._db

    def getDbId(self):
        return self._db.uuid

    def hasDb(self):
        return self._db != None

    def flush(self, 
              into: Type,
              flush_linked: bool = True,
              link_current_depth: int = 0,
              link_max_depth: int = 10,
              set_db: bool = True,
              set_db_if_set: bool = False):
        '''
        Flushes object to some StorageItem.

        Params:
        into: StorageItem

        Returns:
        Storage.DB.Adapters.Connection.ObjectAdapter
        '''

        # We cant annotate this class here, so probaly the StorageItem should have this method? But we have StorageUnit that need to take its files to another dir

        _common = into.getAdapter().flush(self)
        _set_db = True
        if set_db == False:
            _set_db = False
        else:
            if self.hasDb():
                _set_db = set_db_if_set

        # Gets linked items from links list, _db is not set yet
        if flush_linked == True and link_current_depth < link_max_depth:
            for link in self.getLinkedItems():
                link.item.flush(into,
                                link_current_depth,
                                link_max_depth)

                if _set_db == True:
                    link.setDb(_common.addLink(link = link))

        _common.flush_content(self)

        if _set_db == True:
            self.setDb(_common)

        self.flush_hook(into)

        return _common

    def flush_hook(self, into: Type) -> None:
        pass

    @computed_field
    @property
    def db_info(self) -> DBInfo:
        if self.hasDb():
            _db = self.getDb()

            return DBInfo(
                uuid = _db.uuid,
                db_name = _db._adapter._storage_item.name
            )

        return None
