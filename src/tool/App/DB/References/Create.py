from App.Objects.Act import Act
from App.Objects.Arguments.ArgumentDict import ArgumentDict
from App.Objects.Responses.ObjectsList import ObjectsList
from App.Objects.Arguments.Assertions.NotNone import NotNone
from App.Objects.Arguments.ListArgument import ListArgument
from App.Storage.StorageUUID import StorageUUID

class Create(Act):
    @classmethod
    def _arguments(cls) -> ArgumentDict:
        return ArgumentDict(items = [
            ListArgument(
                name = 'uuids',
                orig = StorageUUID,
                assertions = [NotNone()]
            )
        ])

    async def _implementation(self, i):
        res = ObjectsList(items = [])
        for uuid in i.get('uuids'):
            res.append(uuid)

        return res
