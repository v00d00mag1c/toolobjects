from App.Storage.StorageUnit import StorageUnit
from App.Objects.Protocol import Protocol
from App.Objects.Object import Object
from typing import Any
from abc import abstractmethod

class StorageAdapter(Object, Protocol):
    _storage_item: Any = None

    @abstractmethod
    def getStorageUnit(self) -> StorageUnit:
        ...
