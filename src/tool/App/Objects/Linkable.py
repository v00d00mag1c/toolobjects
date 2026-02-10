from pydantic import Field, model_serializer, BaseModel
from App.Objects.Link import Link
from App.Objects.LinkInsertion import LinkInsertion
from collections import deque

class Linkable(BaseModel):
    '''
    Object that can contain links to other objects
    '''

    links: list[Link] = Field(default=[], exclude = True, repr = False)
    #links: deque[Link] = Field(deque(), exclude = True)

    def link(self, object, role: list = []):
        _link = Link(
            item = object,
            role = role
        )
        return self.addLink(_link)

    def unlink(self, item: Link, type: int) -> None:
        pass

    def addLink(self, link: Link) -> None:
        if self.getDb() != None:
            self.getDb().flush(link.item)
            self.getDb().addLink(link)

            return self

        self.links.append(link)

        return link

    def isLinked(self, link: BaseModel) -> bool:
        return True

    def getLinkedItems(self) -> list[Link]:
        '''
        Returns linked items, literally.
        Non-overridable!
        '''

        if self.getDb() != None:
            return list(self.getDb().getLinks())

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

    @model_serializer
    def serialize_model_with_links(self) -> dict:
        result = dict()
        _field_names = list()
        for field_name in self.__class__.model_fields:
            _field_names.append(field_name)
        for field_name in self.__class__.model_computed_fields:
            _field_names.append(field_name)

        for field_name in _field_names:
            value = getattr(self, field_name)

            if isinstance(value, LinkInsertion):
                value.setDb(self.getDb())
                if self._convert_links == True:
                    result[field_name] = value.unwrap()
                else:
                    result[field_name] = value
            elif (isinstance(value, list) and value and isinstance(value[0], LinkInsertion)):
                result[field_name] = []
                for item in value:
                    item.setDb(self.getDb())

                    if self._convert_links == True:
                        result.get('field_name').append(item.unwrap())
            else:
                result[field_name] = value

        return result
