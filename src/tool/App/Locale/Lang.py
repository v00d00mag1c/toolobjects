from App.Objects.Object import Object
from App.Locale.Key import Key
from typing import Any, Optional
from pydantic import Field, PrivateAttr

class Lang(Object):
    name: str = Field()
    native_name: str = Field()
    id: str = Field()
    keys: list[Key] = Field(default = [])
    keys_dict: dict[str, str] = Field(default = {})
    _keys: dict[str, Key] = PrivateAttr(default = {})

    _unserializable = ['keys', 'keys_dict', '_keys']

    def init_hook(self):
        for key_item in self.keys:
            self._keys[key_item.id] = key_item

        # if you don't want to duplicate dict every time
        for key, val in self.keys_dict.items():
            self._keys[key] = Key(
                value = val,
                id = key
            )

    def get(self, key: str, default: Optional[Any] = None) -> str:
        return self._keys.get(key, default)
