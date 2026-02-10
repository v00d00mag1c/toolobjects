from pydantic import Field, BaseModel
from App.Objects.Link import Link

class Linkable:
    '''
    Object that can contain links to other objects
    '''

    links: list[Link] = Field(default=[], exclude = True, repr = False)

    def link(self, object, role: list = []):
        self.addLink(Link(
            item = object,
            role = role
        ))

    def unlink(self, item: Link, type: int) -> None:
        pass

    def addLink(self, item: Link) -> None:
        #if self.links == None:
            #self.links = []

        self.links.append(item)

    def getLinkedItems(self) -> list[Link]:
        '''
        Returns linked items, literally.
        Non-overridable!
        '''
        return self.links

    def getVirtualLinkedItems(self) -> list[Link]:
        '''
        Returns linked items. This method can be overriden
        '''
        return self.getLinkedItems()

    def getLinksRecurisvely(self, current_level = 0, max_depth = 10) -> list[Link]:
        _items = []
        if current_level >= max_depth:
            return []

        for link in self.getLinkedItems():
            _items.append(link)
            _next_links = link.item.getLinksRecurisvely(current_level = current_level + 1, max_depth = max_depth)
            for item in _next_links:
                _items.append(item)

        return _items
