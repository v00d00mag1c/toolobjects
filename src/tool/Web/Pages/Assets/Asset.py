from App.Objects.Object import Object
from App.Storage.StorageUnit import StorageUnit
from abc import abstractmethod

class Asset(Object):
    async def download(self):
        pass

    @abstractmethod
    async def download_function(self, storage_unit: StorageUnit):
        pass
