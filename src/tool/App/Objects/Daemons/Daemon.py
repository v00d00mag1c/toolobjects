from App.Objects.Object import Object
from App.Objects.Executable import Executable
from App.Objects.Arguments.ArgumentValues import ArgumentValues
from App.Storage.StorageUUID import StorageUUID
from pydantic import Field
from App import app
import asyncio

class Daemon(Object):
    item: StorageUUID | Executable = Field(default = None)

    is_stopped: bool = Field(default = True)
    interval: float = Field(default = 10)
    start_iteration: int = Field(default = 0)
    total_iterations: int = Field(default = 0)
    max_iterations: int = Field(default = 0)

    def getModule(self):
        if isinstance(self.item, StorageUUID):
            return self.item.toPython()

        return self.item

    async def iteration(self, iterator_index):
        module = self.getModule()
        _args = ArgumentValues(items=module.args)
        _args.values['iteration'] = iterator_index

        return await module.execute(_args)

    async def start(self) -> dict:
        # move to threading maybe? TODO
        # Returns nothing

        self.is_stopped = False

        self.add_to_daemons()

        reached_end = False
        current_iterator = self.start_iteration

        end_str = '∞'
        if self.is_infinite == False:
            end_str = self.max_iterations

        while reached_end == False and self.is_stopped == False:
            self.total_iterations += 1
            current_iterator += 1
            self.log(f"Run {current_iterator}/{end_str}, interval {self.interval}")

            await self.iteration(current_iterator)

            if self.is_infinite == False:
                reached_end = current_iterator > self.max_iterations

            await asyncio.sleep(self.interval)

        self.remove_from_daemons()

    @property
    def is_infinite(self):
        return self.max_iterations < 1

    def stop(self):
        self.is_stopped = True

    def add_to_daemons(self):
        app.DaemonList.add(self)

    def remove_from_daemons(self):
        app.DaemonList.remove(self)
