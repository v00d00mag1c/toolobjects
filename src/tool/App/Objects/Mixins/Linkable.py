from pydantic import Field, model_serializer, BaseModel
from App.Objects.Relations.Link import Link
from typing import ClassVar, Generator

class Linkable():
    '''
    Object that can contain links to other objects
    '''

    links: list[Link] = Field(default=[], exclude = True, repr = False)
    dynamic_links: bool = Field(default = False)
    supports_dynamic_links: ClassVar[bool] = False

    def link(self, object, role: list = []):
        _link = Link(
            item = object,
            role = role
        )
        return self.addLink(_link)

    '''def __add__(self, object):
        self.link(object)

        return self'''

    def unlink(self, item: Link, role: list = []) -> None:
        _link = Link(
            item = object,
            role = role
        )
        return self.addLink(_link)

    def addLink(self, link: Link) -> Link:
        assert hasattr(link, 'item'), 'link to nothing'

        if self.hasDb() == True:
            if link.item.hasDb() == False:
                self.log('addLink: {0} {1} item is flushed, {2} is not, so we will flush item that we link'.format(self.getClassNameJoined(), self.getDbId(), link.item.getClassNameJoined()))

                link.item.setDb(link.item.flush(self.getDb()._adapter._storage_item))
            else:
                self.log('addLink: both items are flushed')

            if self.sameDbWith(link.item) == False:
                self.log('OK, link item and current item has db, but they are not same, so changing linking item db to current item db')

                link.item.setDb(link.item.flush(self.getDb()._adapter._storage_item))                

            self.getDb().addLink(link)

            return link
        else:
            pass
            #self.log('current item does not has db!')

        self.log('linked items with classes {0}, {1}'.format(self.getClassNameJoined(), link.item.getClassNameJoined()))
        self.links.append(link)

        return link

    def removeLink(self, link: Link) -> bool:
        assert hasattr(link, 'item'), 'unlink from nothing'

        if self.hasDb() == True:
            if link.item.hasDb() == False:
                self.log('can\'t unlink local object and db item')

            self.getDb().removeLink(link)

            return True
        else:
            self.links.remove(link.item)

    def isLinked(self, link: BaseModel) -> bool:
        return True

    def getLinkedItems(self, ignore_db: bool = False) -> Generator[Link]:
        '''
        Returns linked items.
        Non-overridable!
        '''

        if self.getDb() != None and ignore_db == False:
            for item in self.getDb().getLinks():
                yield item

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
