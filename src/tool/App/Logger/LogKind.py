from App.Objects.Object import Object
from pydantic import Field
from enum import Enum

class LogKindEnum(Enum):
    success = 'success'
    error = 'error'
    deprecated = 'deprecated'
    message = 'message'
    highlight = 'highlight'
    bright = 'bright'

class ColorsEnum(Enum):
    red = "\033[91m"
    green = "\033[92m"
    yellow = "\033[93m"
    white = "\033[0m"
    reset = "\033[0m"
    cyan = "\u001b[36m"
    pink = "\u001b[35m"

class LogKind(Object):
    value: LogKindEnum = Field(default = LogKindEnum.message)

    def get_color(self) -> ColorsEnum:
        match(self.value.value):
            case LogKindEnum.error.value:
                return ColorsEnum.red.value
            case LogKindEnum.success.value:
                return ColorsEnum.green.value
            case LogKindEnum.deprecated.value:
                return ColorsEnum.deprecated.value
            case LogKindEnum.highlight.value:
                return ColorsEnum.pink.value
            case LogKindEnum.bright.value:
                return ColorsEnum.cyan.value
            case _:
                return ColorsEnum.white.value
