from App.Objects.Object import Object
from App.Objects.Locale.Key import Key
from pydantic import Field

class Lang(Object):
    name: str = Field()
    self_name: str = Field()
    id: str = Field()
    keys: dict[str, Key] = Field()
