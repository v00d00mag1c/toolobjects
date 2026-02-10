from pydantic import Field, model_serializer, BaseModel
from App.Objects.Link import Link
from collections import deque
from typing import ClassVar, Generator

class Linkable(BaseModel):
    '''
    Object that can contain links to other objects
    '''

    links: list[Link] = Field(default=[], exclude = True, repr = False)
    dynamic_links: bool = Field(default = False)
    supports_dynamic_links: ClassVar[bool] = False
    #links: deque[Link] = Field(deque(), exclude = True)

    def link(self, object, role: list = []):
        _link = Link(
            item = object,
            role = role
        )
        return self.addLink(_link)

    def unlink(self, item: Link) -> None:
        pass

    def addLink(self, link: Link) -> Link:
        if self.getDb() != None:
            link.item.flush(self.getDb()._adapter._storage_item)
            self.getDb().addLink(link)

            return self

        self.links.append(link)

        return link

    def isLinked(self, link: BaseModel) -> bool:
        return True

    def getLinkedItems(self) -> Generator[Link]:
        '''
        Returns linked items, literally.
        Non-overridable!
        '''

        if self.getDb() != None:
            return self.getDb().getLinks()

        for item in self.links:
            yield item

    def getVirtualLinkedItems(self) -> Generator[Link]:
        '''
        Returns linked items. This method can be overriden
        '''
        return self.getLinkedItems()

    def getLinked(self) -> Generator[Link]:
        '''
        Return dynamic links or real links
        '''
        if self.dynamic_links == True:
            return self.getVirtualLinkedItems()
        else:
            return self.getLinkedItems()

    def getLinksRecurisvely(self, current_level = 0, max_depth = 10) -> Generator[Link]:
        if current_level >= max_depth:
            return []

        for link in self.getLinkedItems():
            yield link
            _next_links = link.item.getLinksRecurisvely(current_level = current_level + 1, max_depth = max_depth)
            for item in _next_links:
                yield item
