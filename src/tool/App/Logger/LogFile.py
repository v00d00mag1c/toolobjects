from App.Objects.Object import Object
from pathlib import Path
from pydantic import Field
from datetime import datetime
from typing import Any
from .Log import Log
import json

class LogFile(Object):
    path: str = Field()
    name: str = Field()
    items: list = Field(default = [], exclude = True)
    _update_every_count = 1
    _updated = 0
    _stream: Any = None

    def getPath(self) -> Path:
        extension = '.log.json'

        return Path(self.path).joinpath(self.name + extension)

    @staticmethod
    def autoName(path: str):
        '''
        Auto generates name for logfile
        '''

        now = datetime.now()
        current_name = f"{now.strftime('%Y-%m-%d_%H-%M-%S')}"

        return LogFile(path = str(path), name = current_name)

    def log(self, item: Log):
        self.items.append(item.to_json(mode='json',exclude_none=None,exclude_computed_fields=True,exclude=['class_name__']))
        self._updated += 1

        if self._updated >= self._update_every_count: 
            self._updateFile()
            self._saveFile()
            self._updated = 0
        #self.log_raw(item.model_dump(mode='json',exclude_computed_fields=True,exclude=['class_name__']))

    def open(self):
        _path = self.getPath()
        if _path.exists() == False:
            _tmp = open(_path, 'w', encoding='utf-8')
            _tmp.close()

        self._stream = open(str(_path), 'r+', encoding='utf-8')

    def __del__(self):
        self._updateFile()
        self._saveFile()
        self._stream.close()

    def _updateFile(self):
        self._stream.truncate(0)
        self._stream.seek(0)
        self._stream.write(json.dumps(self.items, indent=4) + '\n')

    def _saveFile(self):
        try:
            self._stream.flush()
        except AttributeError:
            pass
