from App.Storage.StorageUnit import StorageUnit
from App.Objects.Protocol import Protocol
from typing import Any
from abc import abstractmethod

class StorageAdapter(Protocol):
    _storage_item: Any = None

    @abstractmethod
    def getStorageUnit(self) -> StorageUnit:
        ...
