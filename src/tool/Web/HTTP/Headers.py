from App.Objects.Object import Object
from pydantic import Field

class Headers(Object):
    user_agent: str = Field(default='', alias="User-Agent")
