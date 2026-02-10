from App.Objects.Act import Act
from App.Tests.Objects.Migrated.ObjectThatMigrated import ObjectThatMigrated
from App import app

class MigratedTest(Act):
    async def _implementation(self, i):
        _storage = app.Storage.get('tmp')
        _m = ObjectThatMigrated()
        _item = _m.flush(_storage)

        self.log_raw(_item.toPython())
