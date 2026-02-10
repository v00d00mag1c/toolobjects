from App.Objects.Object import Object
from App.Arguments.ArgumentDict import ArgumentDict
from App.Arguments.ArgumentValues import ArgumentValues
from pathlib import Path
from pydantic import Field
from App import app
import json

class Config(Object):
    path: Path = Field()
    name: str = Field(default='config.json')
    values: ArgumentValues = None

    def constructor(self):
        self.values = ArgumentValues(
            compare = ArgumentDict(items=[]),
            values = {},
            raise_on_assertions = False,
            default_on_none = True,
            missing_args_inclusion = True
        )

    def appendSettingsOfModule(self, module) -> None:
        _settings = module.getSettings()
        if _settings != None:
            for item in _settings:
                self.values.compare.append(item)

    @property
    def file(self) -> Path:
        return self.path.joinpath(self.name)

    @classmethod
    def mount(cls):
        configs = cls(
            path = app.app.storage.joinpath("config")
        )
        configs.checkFile()
        configs.appendSettingsOfModule(cls)
        configs.values.values.update(app.app.conf_override)

        app.mount('Config', configs)

        env = Config(
            path = app.app.storage.joinpath("config"),
            name = 'env.json'
        )
        env.checkFile()

        app.mount('Env', env)

    def checkFile(self):
        self.path.mkdir(parents=True,exist_ok=True)
        if self.file.exists() == False:
            temp_stream = open(self.file, 'w', encoding='utf-8')
            default_settings = dict()

            json.dump(default_settings, temp_stream)
            temp_stream.close()

        self._stream = open(self.file, 'r+', encoding='utf-8')
        try:
            self.values.values = json.load(self._stream)
        except json.JSONDecodeError as __exc:
            self.log("failed to load config json")
            #self.reset()

    def updateFile(self) -> None:
        self._stream.seek(0)

        json.dump(self.values.values, self._stream, indent=4)

        self._stream.truncate()

    def reset(self) -> None:
        '''
        Clears all the settings
        '''
        self._stream.seek(0)
        self._stream.write("{}")
        self._stream.truncate()

        self.values.values = {}

    def get(self, option: str, default: str = None):
        got = self.values.get(option)
        if got == None:
            return default

        return got

    def set(self, option: str, value: str):
        if value == None:
            del self.values.values[option]
        else:
            self.values.values[option] = value

        self.updateFile()

    '''
    def updateCompare(self):
        self.comparer.compare = DictList(items = self.getSettingsOfEveryObject())
    '''

    def __del__(self):
        try:
            self._stream.close()
        except AttributeError:
            pass
