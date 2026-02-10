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
    view: Any = None

    def constructor(self):
        _args = self._parse_argv(sys.argv[1:])
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
        from App.Objects.View import View

        '''
        Firstly it creates temp view that allows to mount globals without errors.
        Then it loads ObjectsList. Then it finds needed view and sets is as a common. Then it executes the action of this view.
        The globals are left cuz they are mounted to Wrap.
        '''
        tmp_view = View(app = self)
        tmp_view.setAsCommon()

        self.loadObjects()
        view_name = self.argv.get('view', 'App.Console.ConsoleView')
        view_class = self.objects.getByName(view_name)
        _view: View = view_class

        assert _view != None, 'no such view'

        view = _view.getModule()()
        view.setAsCommon()
        view.setApp(self)

        self.view = view

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
                    path = 'App\\ACL\\AuthLayer.py'
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

        vals = {
            'args': {},
            'conf': {},
            'env': {}
        }
        delimiters = {
            'conf': '--',
            'args': '-',
            'env': ':)'
        }

        _iterate = 0
        _key = None
        _key_dict = None

        for arg in args:
            is_name = _iterate % 2 == 0
            if is_name:
                for key, val in delimiters.items():
                    if arg.startswith(val):
                        _key = arg[len(val):]
                        _key_dict = key

                        break
            else:
                vals.get(_key_dict)[_key] = arg

            _iterate += 1

        return vals.get('args'), vals.get('conf')

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
