from App.Objects.Object import Object
from App.Data.DictList import DictList
from App.Arguments.Comparer import Comparer
from pathlib import Path
from pydantic import Field
from App import app
import json

class Config(Object):
    path: Path = Field()
    name: str = Field(default='config.json')
    comparer: Comparer = None

    def constructor(self):
        self.comparer = Comparer(
            raise_on_assertions = False,
            default_on_none = True,
            missing_args_inclusion = True
        )

    def getSettingsOfEveryObject(self):
        settings = []

        for item in app.app.objects.getList():
            for _item in item.getAllSettings():
                settings.append(_item)

        return settings

    @property
    def file(self) -> Path:
        return self.path.joinpath(self.name)

    @classmethod
    def mount(cls):
        configs = cls(
            path = app.app.storage.joinpath("config")
        )
        configs.checkFile()
        configs.updateCompare()
        configs.comparer.values.update(app.app.conf_override)

        app.mount('Config', configs)

        env = Config(
            path = app.app.storage.joinpath("config"),
            name = 'env.json'
        )
        env.checkFile()
        env.updateCompare()

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
            self.comparer.values = json.load(self._stream)
        except json.JSONDecodeError as __exc:
            self.log("failed to load config json")
            #self.reset()

    def updateFile(self) -> None:
        self._stream.seek(0)

        # double "toDict()" cuz firstly we get ArgumentsDict and then getting actual dict

        json.dump(self.comparer.toDict().toDict(), self._stream, indent=4)

        self._stream.truncate()

    def reset(self) -> None:
        '''
        Clears all the settings
        '''
        self._stream.seek(0)
        self._stream.write("{}")
        self._stream.truncate()

        self.comparer.values = {}

    def get(self, option: str, default: str = None):
        got = self.comparer.getByName(option)
        if got == None:
            return default

        return got

    def set(self, option: str, value: str):
        if value == None:
            del self.comparer.values[option]
        else:
            self.comparer.values[option] = value

        self.updateFile()

    def updateCompare(self):
        self.comparer.compare = DictList(items = self.getSettingsOfEveryObject())

    def __del__(self):
        try:
            self._stream.close()
        except AttributeError:
            pass
