from App.Objects.Object import Object
from App.Locale.Key import Key
from typing import Any, Optional
from pydantic import Field, PrivateAttr

class Lang(Object):
    name: str = Field()
    native_name: str = Field()
    id: str = Field()
    keys: list[Key] = Field()
    _keys: dict[str, Key] = PrivateAttr(default = {})

    _unserializable = ['keys', '_keys']

    def init_hook(self):
        for key_item in self.keys:
            self._keys[key_item.id] = key_item

    def get(self, key: str, default: Optional[Any] = None) -> str:
        return self._keys.get(key, default)
