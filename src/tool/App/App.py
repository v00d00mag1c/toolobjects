from App.Objects.Object import Object
from App.Objects.Index.LoadedObject import LoadedObject
from App.Arguments.ArgumentValues import ArgumentValues
from App.Objects.Increment import Increment
from App.Objects.Index.Namespace import Namespace
from pathlib import Path
from pydantic import ConfigDict
from typing import Any
import queue
import asyncio
import threading
import sys
import os

class App(Object):
    # Pathes
    cwd: str = None
    src: str = None
    storage: str = None
    acl: str = None

    # Args
    argv: dict = None
    conf_override: dict = None

    # Internal
    loop: Any = None
    hook_thread: Any = None
    executables_id: Increment = None

    def constructor(self):
        _args = self._parse_argv(sys.argv)
        self.argv = _args[0]
        self.conf_override = _args[1]
        #self.cwd = Path(os.getcwd())
        self.cwd = Path(__file__).parent.parent # objects dir
        self.src = self.cwd.parent # "tool", "storage", "venv" and update scripts
        self.acl = self.src.joinpath('acl')
        self.storage = self.src.joinpath('storage') # default storage
        self.storage.mkdir(exist_ok = True)
        self.loop = asyncio.new_event_loop()
        self.executables_id = Increment()
        self.hook_thread = HookThread()

    def loadView(self) -> None:
        from App.View import View

        '''
        Firstly it creates temp view that allows to mount globals without errors.
        Then it loads ObjectsList. Then it finds needed view and sets is as a common. Then it executes the action of this view.
        The globals are left cuz they are mounted to Wrap.
        '''
        tmp_view = View(app = self)
        tmp_view.setAsCommon()

        self.loadObjects()
        view_name = self.argv.get('view', 'App.Console.Console.Console')
        view_class = self.objects.getByName(view_name)
        view: View = view_class.getModule()()
        view.setAsCommon()
        view.setApp(self)

        return view

    def loadObjects(self):
        self.objects = Namespace(
            name = 'common',
            root = str(self.cwd),
            load_once = False,
            ignore_dirs = ['Custom'],
            load_before = [
                LoadedObject(
                    path = 'App\\Storage\\Config.py'
                ),
                LoadedObject(
                    path = 'App\\Logger\\Logger.py'
                ),
                LoadedObject(
                    path = 'Web\\DownloadManager\\Manager.py'
                )
            ],
            load_after = [
                LoadedObject(
                    path = 'App\\Objects\\Index\\ObjectsList.py'
                ),
                LoadedObject(
                    path = 'App\\Objects\\Index\\ExecutablesList.py'
                ),
                LoadedObject(
                    path = 'App\\Storage\\Storage.py'
                ),
                LoadedObject(
                    path = 'App\\Objects\\Index\\PostRun.py'
                )
            ]
        )
        self.objects.load()

    async def runView(self, view) -> None:
        await view.execute(ArgumentValues(values = self.argv))

    def _parse_argv(self, args):
        '''
        "-arg1 val1" - argument to the View
        "--arg1 val1" - argument to config
        '''

        ARGS = {}
        CONF_VALS = {}

        # sep.2024
        ARG_DELIMITER = '-'
        CONF_VAL_DELIMITER = '--'

        key = None
        key_type = None

        for arg in args[1:]:
            if arg.startswith(CONF_VAL_DELIMITER):
                if key:
                    ARGS[key] = True
                key = arg[2:]
                key_type = CONF_VAL_DELIMITER
                CONF_VALS[key] = True
            elif arg.startswith(ARG_DELIMITER):
                if key:
                    ARGS[key] = True
                key = arg[1:]
                key_type = ARG_DELIMITER
                ARGS[key] = True
            else:
                if key:
                    if key_type == ARG_DELIMITER:
                        ARGS[key] = arg
                    else:
                        CONF_VALS[key] = arg

                    key = None
                    key_type = None
                else:
                    pass

        return ARGS, CONF_VALS

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
