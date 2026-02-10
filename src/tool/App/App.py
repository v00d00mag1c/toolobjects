from App.Objects.Object import Object
from App.Objects.Section import Section
from pathlib import Path
from typing import Any
import asyncio
import sys
import os

class App(Object):
    argv: dict = None
    cwd: str = None
    src: str = None
    loop: Any = None
    objects: list = None

    def _constructor(self):
        self.argv = self._parse_argv()
        self.cwd = Path(os.getcwd())
        self.src = self.cwd.parent
        self.loop = asyncio.get_event_loop()

    def _parse_argv(self):
        # didn't changed since sep.2024
        args = sys.argv
        parsed_args = {}
        key = None
        for arg in args[1:]:
            if arg.startswith('--'):
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

    def load_plugins(self):
        from .Index.List import List

        self.objects = List()
        self.objects.load()
