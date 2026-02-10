from App.Objects.Executable import Executable
from App.Objects.Wheel import Wheel
from typing import ClassVar

class Client(Wheel):
    self_name: ClassVar[str] = 'Client'
