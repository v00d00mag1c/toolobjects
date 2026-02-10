from App.Objects.Object import Object
from App.Objects.Executable import Executable
from App.Objects.Arguments.ArgumentValues import ArgumentValues
from App.Storage.StorageUUID import StorageUUID
from pydantic import Field
from App import app
import asyncio

class DaemonItem(Object):
    item: StorageUUID | Executable = Field(default = None)

    interval: float = Field(default = 10)
    start_iteration: int = Field(default = 0)
    total_iterations: int = Field(default = 0)
    max_iterations: int = Field(default = 0)

    def getModule(self):
        if isinstance(self.item, StorageUUID):
            return self.item.toPython()

        return self.item
