from App.Objects.Object import Object
from App.Objects.Arguments.Argument import Argument
from App.Objects.Arguments.ArgumentValues import ArgumentValues
from App.Objects.Arguments.ArgumentDict import ArgumentDict

from pydantic import Field
from pathlib import Path
from typing import Literal
import json

class ConfigItem(Object):
    path: Path = Field(default=None)
    name: str = Field(default='config.json')
    role: Literal['config', 'env'] = Field()
    values: ArgumentValues = Field(default=None)
    enabled: bool = Field(default = True)

    @property
    def file(self) -> Path:
        return self.path.joinpath(self.name)

    def init_hook(self):
        if self.values == None:
            self.values = ArgumentValues(
                compare = ArgumentDict(items=[]),
                values = {},
                raise_on_assertions = False,
                default_on_none = True,
                missing_args_inclusion = True
            )

    def updateFile(self) -> None:
        self._stream.seek(0)

        json.dump(self.values.values, self._stream, indent=4, ensure_ascii=False)

        self._stream.truncate()

    def reset(self) -> None:
        '''
        Clears all the settings
        '''
        self._stream.seek(0)
        self._stream.write("{}")
        self._stream.truncate()

        self.values.values = {}

    def get(self, option: str, default: str = None, raw: bool = False):
        got = self.values.get(option)
        if raw == True:
            got = self.values.values.get(option)
        if got == None:
            return default

        return got

    def set(self, option: str, value: str, save_old_values: bool = False):
        if save_old_values:
            _val = self.values.values.get(option)
            self.values.values[option + '.old'] = _val

        if value == None:
            del self.values.values[option]
        else:
            self.values.values[option] = value

        self.updateFile()

    def check_file(self):
        self.path.mkdir(exist_ok = True)
        if self.file.exists() == False:
            temp_stream = open(self.file, 'w', encoding='utf-8')
            default_settings = dict()

            json.dump(default_settings, temp_stream)
            temp_stream.close()

        self._stream = open(self.file, 'r+', encoding='utf-8')
        try:
            self.values.values = json.load(self._stream)
        except json.JSONDecodeError as __exc:
            self.log_error("failed to load config json")
            #self.reset()

    def append_settings_of_module(self, module) -> None:
        _settings = module._settings()
        if _settings != None:
            for item in _settings:
                self.values.compare.append(item)

    def append_compare(self, item: Argument):
        self.values.compare.append(item)

    def __del__(self):
        try:
            self._stream.close()
        except AttributeError:
            pass
