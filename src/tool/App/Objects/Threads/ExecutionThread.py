from App.Objects.Object import Object
from App.Logger.LogPrefix import LogPrefix
from typing import Type, Coroutine, Optional, Any
from concurrent.futures import Future
from pydantic import Field
from App import app
import threading
import asyncio
import queue

class ExecutionThread(Object):
    '''
    Wrapper of the executable run
    '''

    thread: Any | Type[threading.Thread] = Field(default = None)
    result_future: Any | Type[Future] = Field(default = None)
    stop_event: Any | Type[threading.Event] = Field(default = None)
    result_queue: Any | Type[queue.Queue] = Field(default = None)
    exception: Any | Type[Exception] = Field(default = None)

    id: int = Field()

    _unserializable = ['thread', 'result_future', 'stop_event', 'result_queue', 'exception', 'id']

    @property
    def append_prefix(self) -> LogPrefix:
        return LogPrefix(
            id = self.id,
            name = 'ID'
        )

    def set(self, func: Coroutine):
        def _run():
            try:
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                try:
                    if asyncio.iscoroutine(func):
                        result = loop.run_until_complete(func)
                    else:
                        result = func()

                    self.result_future.set_result(result)
                    self.result_queue.put(('result', result))

                except Exception as e:
                    self.result_future.set_exception(e)
                    self.result_queue.put(('error', e))
                    self.exception = e

                finally:
                    loop.close()
            except Exception as e:
                self.result_future.set_exception(e)
                self.result_queue.put(('error', e))
                self.exception = e

        self.thread = threading.Thread(target=_run, daemon = True)
        self.result_future = Future()
        self.stop_event = threading.Event()
        self.result_queue = queue.Queue()

        if app.ExecutablesList != None:
            app.ExecutablesList.add(self)

    def end(self):
        self.stop_event.set()

        if app.ExecutablesList != None:
            app.ExecutablesList.remove(self)

    async def get(self, timeout: Optional[float] = None):
        self.log('Running execution thread')

        assert self.thread != None, 'this thread is unavailable'
        assert self.thread.is_alive() == False, 'this thread is already running'

        self.thread.start()
        self.thread.join(timeout)

        if self.thread.is_alive():
            raise TimeoutError(f"Thread execution timeout after {timeout} seconds")
        try:
            return self.result_future.result(timeout=0)
        except Exception as e:
            if self.exception:
                raise self.exception
            raise e
