from App.Objects.Object import Object
from App.Objects.Arguments.ArgumentDict import ArgumentDict
from App.Objects.Relations.Submodule import Submodule
from App.Objects.Queue.Queue import Queue
from typing import Optional
from pydantic import Field

class CustomObject(Object):
    name: str = Field(default = None)
    extends_from: list[str] = Field(default = ['App.Objects.Object'])
    arguments: Optional[ArgumentDict] = Field(default = None)
    submodules: Optional[list[Submodule]] = Field(default = None)
    execution: Optional[Queue] = Field(default = None)

    async def execute(self, i):
        if self.execution:
            return await self.execution.run(i)
        else:
            if hasattr(super, 'execute'):
                return await super().execute(i)
            else:
                raise AssertionError('object does not contains execution interface')
