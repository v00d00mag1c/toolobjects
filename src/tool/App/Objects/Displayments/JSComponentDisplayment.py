from App.Objects.Displayments.Displayment import Displayment
from pydantic import Field

class JSComponentDisplayment(Displayment):
    role: list[str] = Field(default = ['js'])
