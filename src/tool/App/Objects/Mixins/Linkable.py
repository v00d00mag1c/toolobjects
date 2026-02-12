from pydantic import Field, model_serializer, BaseModel
from App.Objects.Relations.Link import Link
from App.Objects.Relations.LinkData import LinkData
from typing import ClassVar, Generator, AsyncGenerator

class Linkable():
    '''
    Object that can contain links to other objects
    '''

    supports_dynamic_links: ClassVar[bool] = False

    def link(self, object, role: list = []):
        _link = Link(
            item = object,
            data = LinkData(
                role = role
            )
        )
        return self.addLink(_link)

    def unlink(self, item: Link, role: list = []) -> None:
        _link = Link(
            item = item,
            data = LinkData(
                role = role
            )
        )
        return self.removeLink(_link)

    def addLink(self, link: Link) -> Link:
        assert hasattr(link, 'item'), 'link to nothing'

        if self.hasDb() == True:
            if link.item.hasDb() == False:
                self.log('addLink: {0} {1} item is flushed, {2} is not, so we will flush item that we link'.format(self._getClassNameJoined(), self.getDbId(), link.item._getClassNameJoined()), role = ['flushed'])

                link.item.setDb(link.item.flush(self.getDb()._adapter._storage_item))
            #else:
                #self.log('addLink: both items are flushed')

            if self.sameDbWith(link.item) == False:
                self.log('OK, link item and current item has db, but they are not same, so changing linking item db to current item db', role = ['flushed'])

                link.item.setDb(link.item.flush(self.getDb()._adapter._storage_item))                

            self.getDb().addLink(link)

            return link
        else:
            pass
            #self.log('current item does not has db!')

        self.log('linked items with classes {0}, {1}'.
                 format(self._getClassNameJoined(), link.item._getClassNameJoined()), 
                 role = ['flushed', 'linked_items'])

        self.local_obj.links.append(link)

        return link

    def removeLink(self, link: Link) -> bool:
        assert hasattr(link, 'item'), 'unlink from nothing'

        if self.hasDb() == True:
            if link.item.hasDb() == False:
                self.log('can\'t unlink local object and db item')

            self.getDb().removeLink(link)

            return True
        else:
            self.local_obj.links.remove(link.item)

    def isLinked(self, item: BaseModel) -> bool:
        return self.find_link(item) != None

    def find_link(self, item: BaseModel, role: list = None) -> Link:
        for link in self.getLinkedItems():
            if role != None:
                if ','.join(role) != ','.join(link.data.role):
                    continue

            if link.item.hasDb():
                assert link.item.getDbName() == item.getDbName(), 'cross db'

                if link.item.getDbId() == item.getDbId():
                    return link
            else:
                if link.item == item:
                    return link

    def getLinkedItems(self, ignore_db: bool = False, with_role: str = None) -> Generator[Link]:
        '''
        Returns linked items.
        Non-overridable!
        '''

        if self.getDb() != None and ignore_db == False:
            for item in self.getDb().getLinks(with_role = with_role):
                _item = item.toPython()

                if _item == None:
                    continue

                if with_role:
                    _role = list()
                    if type(_item.data) != list:
                        _role = _item.data.get('role', [])

                    if with_role not in _role:
                        continue

                yield _item
        else:
            for item in self.local_obj.links:
                if with_role:
                    if with_role not in item.data.role:
                        continue

                yield item

    async def _get_virtual_linked(self, with_role: str = None) -> AsyncGenerator[Link]:
        '''
        Returns linked items. This method can be overriden
        '''

        for item in self.getLinkedItems():
            yield item

    def getLinked(self, ignore_virtual: bool = False, with_role: str = None) -> Generator[Link]:
        '''
        Return dynamic links or real links.
        No, dynamic links are getting from asyncGetLinked.
        '''
        #if self.local_obj.dynamic_links == True and ignore_virtual == False:
            #return self._get_virtual_linked(with_role = with_role)
        #else:
        return self.getLinkedItems(with_role = with_role)

    async def asyncGetLinked(self, ignore_virtual: bool = False, with_role: str = None):
        if self.local_obj.dynamic_links == True and ignore_virtual == False:
            async for item in self._get_virtual_linked(with_role = with_role):
                yield item
        else:
            for item in self.getLinkedItems(with_role = with_role):
                yield item

    def getLinksRecurisvely(self, current_level = 0, max_depth = 10) -> Generator[Link]:
        if current_level >= max_depth:
            return []

        for link in self.getLinkedItems():
            yield link
            _next_links = link.item.getLinksRecurisvely(current_level = current_level + 1, max_depth = max_depth)
            for item in _next_links:
                yield item
