from App.Objects.Object import Object
from App.Objects.Section import Section
from pathlib import Path
from pydantic import ConfigDict
from typing import Any
from .Index.List import List as ObjectsList
import queue
import asyncio
import threading
import sys
import os

class App(Object):
    argv: dict = None
    cwd: str = None
    src: str = None
    storage: str = None
    loop: Any = None
    objects: ObjectsList = None
    hook_thread: Any = None

    def _constructor(self):
        self.argv = self._parse_argv(sys.argv)
        self.cwd = Path(os.getcwd())
        self.src = self.cwd.parent
        self.storage = self.src.joinpath('storage')
        self.storage.mkdir(exist_ok = True)
        self.loop = asyncio.new_event_loop()

        self.hook_thread = HookThread()

    def _parse_argv(self, args):
        # didn't changed since sep.2024
        delimiter = '--'
        parsed_args = {}
        key = None
        for arg in args[1:]:
            if arg.startswith(delimiter):
                if key:
                    parsed_args[key] = True
                key = arg[2:]
                parsed_args[key] = True
            else:
                if key:
                    parsed_args[key] = arg
                    key = None
                else:
                    pass

        return parsed_args

    def load_plugins(self, search_dir: Path):
        self.objects = ObjectsList()
        self.objects.load(search_dir)

class HookThread():
    '''
    It allows to use hooks without await things, but also it provides bad sync in main thread
    '''

    def __init__(self):
        self.task_queue = queue.Queue()
        self.running = True
        self.thread = threading.Thread(target=self._loop, daemon=True)
        self.thread.start()

    def _loop(self):
        self.running_loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.running_loop)

        while self.running:
            try:
                hook_func, args, kwargs = self.task_queue.get(timeout=0.5)

                try:
                    if asyncio.iscoroutinefunction(hook_func):
                        self.running_loop.run_until_complete(hook_func(*args, **kwargs))
                    else:
                        hook_func(*args, **kwargs)
                except Exception as e:
                    pass
                finally:
                    self.task_queue.task_done()
            except queue.Empty:
                continue
