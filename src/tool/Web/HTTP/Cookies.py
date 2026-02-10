from App.Objects.Object import Object
from pydantic import Field

class Cookies(Object):
    domain: str = Field(default = None)
    values: dict = Field(default = {})
