from App.Objects.Object import Object
from pydantic import Field

class LogSection(Object):
    value: list = Field(repr=True, default = ['N/A'])

    def join(self) -> str:
        return "!".join(self.value)

    def toString(self) -> str:
        return f"[{self.join()}]"
