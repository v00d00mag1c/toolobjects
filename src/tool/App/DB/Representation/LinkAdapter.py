from App.Objects.Relations.Link import Link
from Data.Types.JSON import JSON
from abc import abstractmethod
from App.DB.Representation.AbstractAdapter import AbstractAdapter
from App.DB.Representation.ObjectAdapter import ObjectAdapter

class LinkAdapter(AbstractAdapter):
    owner: int = None
    target: int = None
    data: str = None
    order: int = None

    @abstractmethod
    def getTarget(self) -> ObjectAdapter:
        pass

    def _parseData(self) -> list:
        if self.data != None:
            return JSON().fromText(self.data)

        return []

    def toPython(self) -> Link:
        _role = self._parseData()
        _target = self.getTarget()
        if _target == None:
            return None

        _link = Link(item = None)
        _link.item = _target.toPython()
        _link.data = _role
        _link.setDb(self)

        return _link

    @abstractmethod
    def reorder(self, order: int):
        self.order = order

    @abstractmethod
    def deleteFromDB(self, remove_links: bool = False):
        ...
