from App.Objects.Act import Act
from App.Objects.Protocol import Protocol
from abc import abstractmethod
from App.Objects.Responses.ObjectsList import ObjectsList

class ExplorerProtocol(Act, Protocol):
    @abstractmethod
    def implementation(self, i) -> ObjectsList:
        ...
