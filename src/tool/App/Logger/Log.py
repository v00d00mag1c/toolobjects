from App.Objects.Object import Object
from . import LogKind, LogSection, LogPrefix
from pydantic import Field
from datetime import datetime

class Log(Object):
    '''
    message - passed message
    time - when log was created
    kind - type (error, success, message)
    section - class name where log was taken
    prefix - additional data
    types - internal type of log (not used)
    '''

    message: str = Field(default="-")
    role: list[str] = Field(default = [])
    time: datetime = Field(default_factory=lambda: datetime.now())
    kind: LogKind.LogKind = Field(default = LogKind.LogKind())
    section: LogSection.LogSection = Field(default = LogSection.LogSection())
    prefix: LogPrefix.LogPrefix = Field(default = None)

    def toParts(self) -> list[str]:
        KIND_COLOR = self.kind.get_color()
        RESET = LogKind.ColorsEnum.reset.value

        parts = []
        parts.append(self.time.strftime("%H:%M:%S.%f"))        
        parts.append(LogKind.ColorsEnum.pink.value + self.section.toString() + RESET)
        if self.prefix != None:
            parts.append(LogKind.ColorsEnum.cyan.value + self.prefix.toString() + RESET)

        parts.append(KIND_COLOR + self.message + RESET)
        parts.append(RESET)

        return parts

    def toStr(self) -> str:
        return " ".join(self.toParts()).replace("\\n", "\n")
