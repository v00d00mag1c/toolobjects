from App.Objects.Saveable import Saveable
from pydantic import Field

class Text(Saveable):
    text: str = Field(default = '')
