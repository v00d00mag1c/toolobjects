from App.Storage.StorageUnit import StorageUnit
from App.Objects.Protocol import Protocol
from App.Objects.Object import Object
from typing import Any, Generator
from abc import abstractmethod
from pathlib import Path

class StorageAdapter(Object, Protocol):
    _storage_item: Any = None

    @abstractmethod
    def get_all_files(self) -> Generator[Path]:
        ...

    @abstractmethod
    def get_storage_unit(self) -> StorageUnit:
        ...

    @abstractmethod
    def copy_storage_unit(self, unit: StorageUnit, change_common: bool = True):
        ...

    @abstractmethod
    def clear(self, recreate: bool = True):
        ...

    @abstractmethod
    def destroy(self):
        ...

    @abstractmethod
    def get_relative_path(self, path: Path):
        ...

    @abstractmethod
    def get_size(self) -> int:
        ...
