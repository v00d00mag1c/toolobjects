from App.Objects.Object import Object
from App.Objects.Arguments.ArgumentValues import ArgumentValues
from App.Objects.Arguments.ListArgument import ListArgument
from App.Storage.ConfigItem import ConfigItem

from pathlib import Path
from pydantic import Field
from typing import Literal, Any
from App import app

class Config(Object):
    items: list[ConfigItem] = Field(default = [])
    common: int = 0
    common_env: int = 1

    @classmethod
    def mount(cls):
        _pre = [
            ConfigItem(
                path = app.app.storage.joinpath("config"),
                role = 'config',
                name = 'config.json',
            ),
            ConfigItem(
                path = app.app.storage.joinpath("config"),
                role = 'env',
                name = 'env.json'
            )
        ]
        _pre[0].append_settings_of_module(cls)

        config_switcher = cls()
        app.mount('Config', config_switcher)

        for item in _pre + _pre[0].get('app.config.items'):
            config_switcher.items.append(item)

            item.check_file()

        _pre[0].values.values.update(app.app.conf_override)

    # 2many arguments cycles
    def get(self, name: str, default: Any = None, role: str = 'config'):
        return self.getItem(role = role).get(name, default)

    def set(self, name: str, value: Any = None, role: str = 'config'):
        return self.getItem(role = role).set(name, value)

    def getItem(self, role: Literal['config', 'env'] = 'config'):
        if role == 'config':
            return self.items[self.common]
        elif role == 'env':
            return self.items[self.common_env]
        else:
            return None

    @classmethod
    def _settings(cls):
        return [
            ListArgument(
                name = 'app.config.items',
                default = [],
                orig = ConfigItem
            )
        ]
