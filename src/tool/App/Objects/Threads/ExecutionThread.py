from App.Objects.Object import Object
from App.Logger.LogPrefix import LogPrefix
from typing import Type, Coroutine, Optional, Any
from concurrent.futures import Future
from pydantic import Field
from App import app
import asyncio

class ExecutionThread(Object):
    '''
    Wrapper of the executable run
    '''

    task: Any | Type[asyncio.Task] = Field(default = None)
    is_stopped: bool = Field(default = False)
    cancelled: bool = Field(default = False)

    id: int = Field()
    global_id: int = Field(default = None)
    name: str = Field(default = 'Untitled')
    timeout: Optional[float] = Field(default = None)

    _unserializable = ['task']

    @property
    def append_prefix(self) -> LogPrefix:
        return LogPrefix(
            id = self.global_id,
            name = 'ID'
        )

    def set(self, func: Coroutine):
        if app.ThreadsList != None:
            app.ThreadsList.add(self)

        self.task = asyncio.create_task(self._execute_wrapper(func))

    def set_name(self, name: str):
        self.name = name

    async def _execute_wrapper(self, coroutine: Coroutine):
        try:
            result = await coroutine
            return result
        except asyncio.CancelledError:
            self.log_error('Task {0} was cancelled'.format(self.global_id))
        except Exception as e:
            raise e
        finally:
            if app.ThreadsList is not None:
                app.ThreadsList.remove(self)

    def end(self):       
        if self.task and not self.task.done():
            self.task.cancel()

        if app.ThreadsList != None:
            app.ThreadsList.remove(self)

    async def get(self):
        self.log('running thread', role = ['thread'])

        if self.task is None:
            raise RuntimeError("Task is not set")

        if self.task.done():
            return await self.task

        try:
            if self.timeout is not None:
                return await asyncio.wait_for(self.task, self.timeout)
            else:
                return await self.task
        except asyncio.CancelledError:
            self.cancelled = True
            raise
        except Exception as e:
            self.log(f"Task raised exception")
            raise
