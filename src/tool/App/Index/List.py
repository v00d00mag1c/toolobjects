from App.Objects.Object import Object
from Data.Increment import Increment
from Data.DictList import DictList
from App import app
from pathlib import Path
from typing import Generator
from .LoadedObject import LoadedObject

class List(Object):
    id: Increment = None
    items: DictList = None
    calls: list = []

    def constructor(self):
        self.id = Increment()
        self.items = DictList(items = [])

    def load(self, search_dir: Path):
        # traceback.print_list(traceback.extract_stack())

        self.log("Loading objects list...")

        for item_path in self.scan(search_dir):
            plugin = LoadedObject.from_path(item_path)

            try:
                plugin.module = plugin.get_module()
                plugin.succeed_load()
            except Exception as e:
                plugin.failed_load(e)

            self.items.append(plugin)

    def scan(self, path: Path) -> Generator[Path]:
        items: list = list()
        files = path.rglob('*.py')
        priority_names: list = ['App\\Config\\Config.py', 'App\\Logger\\Logger.py', 'App\\Env\\Env.py', 'App\\Storage\\Storage.py', 'App\\DB\\Connection.py', 'Web\\DownloadManager\\DownloadManager.py']
        priority = [path.joinpath(p) for p in priority_names]

        # 1st iteration
        for plugin in files:
            # 2nd iteration
            if plugin not in priority:
                items.append(plugin)

        # adding priority and plugins that are not in priority. Its better to do sort there*?
        for plugin in  items:
            # hardcoded check
            if plugin.name in ['', '__pycache__', 'Base.py', 'cli.py']:
                continue

            yield plugin.relative_to(path)
