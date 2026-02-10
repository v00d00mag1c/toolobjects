from App.Objects.Act import Act
from App.DB.Search import Search
from App.Objects.Arguments.ArgumentDict import ArgumentDict
from App.Objects.Responses.ObjectsList import ObjectsList
from App.Storage.StorageUUID import StorageUUID

class SearchOnlyIds(Act):
    @classmethod
    def _arguments(cls) -> ArgumentDict:
        return ArgumentDict(missing_args_inclusion=True)

    async def implementation(self, i):
        _list = ObjectsList()
        _search = Search()
        _items = await _search.execute(i)

        for item in _items.getItems():
            _list.append(StorageUUID(storage = i.get('storage'), uuid = item.getDbId()))

        return _list
