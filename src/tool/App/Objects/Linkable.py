from pydantic import Field, BaseModel
from App.Objects.Link import Link

class Linkable:
    '''
    Object that can contain links to other objects
    '''

    links: list[Link] = Field(default=[], exclude = True)

    def addLink(self, item: Link) -> None:
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

    def linkItem(self, object, link_type: int):
        pass

    def addCommonLink(self, item: Link) -> None:
        pass

    def unlink(self, item: Link, type: int) -> None:
        pass
