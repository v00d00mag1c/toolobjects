from typing import Any, Type
from pydantic import computed_field
from App.DB.DBInfo import DBInfo

class DBInsertable():
    _db: Any = None  # : ObjectAdapter

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

    def getDbId(self, as_str: bool = False):
        if as_str:
            return str(self._db.uuid)

        return self._db.uuid

    def getDbName(self):
        return self._db._adapter._storage_item.name

    def getDbIds(self):
        return '{0}_{1}'.format(self.getDbName(), self.getDbId())

    def hasDb(self):
        return self._db != None

    def sameDbWith(self, item):
        return self.getDb()._adapter._storage_item.name == item.getDb()._adapter._storage_item.name

    def flush(self, 
              into: Type,
              flush_linked: bool = True,
              link_current_depth: int = 0,
              link_max_depth: int = 10,
              set_db: bool = True,
              set_db_if_set: bool = False,
              ignore_flush_hooks: bool = False):
        '''
        Flushes object to some StorageItem.

        Params:
        into: StorageItem

        Returns:
        DB.Adapters.Connection.ObjectAdapter
        '''

        # We cant annotate this class here, so probaly the StorageItem should have this method? But we have StorageUnit that need to take its files to another dir

        _db_item = into.get_db_adapter().flush(self)
        _set_db = True
        # ???
        if set_db == False:
            _set_db = False
        else:
            if self.hasDb():
                _set_db = set_db_if_set

        _id = 0
        # Gets linked items from links list, _db is not set yet
        if flush_linked == True and link_current_depth < link_max_depth and hasattr(self, 'getLinkedItems'):
            for link in self.getLinkedItems():
                try:
                    # If link item exists, but the link is not exists in db.
                    if link.item.hasDb() and link.item.getDbName() != into.name:
                        self.log('flush: links: the link item is already flushed')
                    else:
                        link.item.flush(into,
                                        flush_linked,
                                        link_current_depth = link_current_depth,
                                        link_max_depth = link_max_depth,
                                        set_db = set_db,
                                        ignore_flush_hooks = ignore_flush_hooks)

                    if link.hasDb() == False or _set_db == True:
                        link.setDb(_db_item.addLink(link = link))

                    self.log('flush: links: flushed link with id {0}, order {1}'.format(link.getDbId(), _id), role = ['flushed', 'flushing.link'])

                    _id += 1
                except Exception as e:
                    self.log_error(e)

        _db_item.flush_content(self)
        if _set_db == True:
            self.setDb(_db_item)

        if ignore_flush_hooks == False:
            self.flush_hook(into)

        _role = ['flushed']
        if into.name == 'tmp':
            _role.append('storage.flushing.tmp')

        self.log(f"flushed item", role = _role)

        return _db_item

    def delete(self, remove_links: bool = True, commit: bool = False):
        if self.hasDb() == False:
            return

        self.getDb().deleteFromDB(remove_links = remove_links)
        self.deletion_hook()
        if commit == True and self._db._adapter.auto_commit == False:
            self._db._adapter.commit()

    def save(self, do_commit: bool = True) -> bool:
        '''
        Updates linked db item if exists (save_hook)
        '''

        self.save_hook()

        if self.hasDb() == False:
            return True

        self.getDb().flush_content(self)
        if do_commit and self._db._adapter.auto_commit == False:
            self._db._adapter.commit()

        return True

    def flush_hook(self, into: Type) -> None:
        pass

    def deletion_hook(self) -> None:
        pass

    def save_hook(self) -> None:
        # Runs before save
        pass
