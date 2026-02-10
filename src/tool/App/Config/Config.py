from App.Objects.Object import Object
from App.Objects.Arguments.ArgumentValues import ArgumentValues
from App.Objects.Arguments.ListArgument import ListArgument
from App.Config.ConfigItem import ConfigItem

from pathlib import Path
from pydantic import Field
from typing import Literal, Any
from App import app

class Config(Object):
    loaded_module_names: list[str] = Field(default = [])
    items: list[ConfigItem] = Field(default = [])
    common: int = 0
    common_env: int = 1

    @classmethod
    def mount(cls):
        _pre = [
            ConfigItem(
                path = app.app.src.joinpath("config"),
                role = 'config',
                name = 'config.json',
            ),
            ConfigItem(
                path = app.app.src.joinpath("config"),
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

    def appendModule(self, module):
        if module._getNameJoined() in self.loaded_module_names:
            pass
            #self.log('{0} already loaded'.format(module._getNameJoined()))

        try:
            self.loaded_module_names.append(module._getNameJoined())

            _settings = module.getSettings()
            for _item in _settings:
                self.getItem(role = _item.role).append_compare(_item)
        except Exception as e:
            self.log_error(e)

    @classmethod
    def _settings(cls):
        return [
            ListArgument(
                name = 'app.config.items',
                default = [],
                orig = ConfigItem
            )
        ]
