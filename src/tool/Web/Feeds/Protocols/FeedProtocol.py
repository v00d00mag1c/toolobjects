from App.Objects.Object import Object
from App.Objects.Protocol import Protocol
import xml.etree.ElementTree as ET
from abc import abstractmethod

class FeedProtocol(Object, Protocol):
    @abstractmethod
    async def _get_channels(self, data: ET):
        ...
