from pydantic import Field, model_serializer, BaseModel
from App.Objects.Link import Link
from App.Objects.LinkInsertion import LinkInsertion

class Linkable(BaseModel):
    '''
    Object that can contain links to other objects
    '''

    links: list[Link] = Field(default=[], exclude = True, repr = False)

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

    def getLinkedItems(self) -> list[Link]:
        '''
        Returns linked items, literally.
        Non-overridable!
        '''

        if self.getDb() != None:
            return self.getDb().getLinks()

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
        for field_name in self.__class__.model_fields:
            value = getattr(self, field_name)

            if self._convert_links == True:
                if isinstance(value, LinkInsertion):
                    result[field_name] = value.unwrap()
                elif isinstance(value, list) and value and isinstance(value[0], LinkInsertion):
                    result[field_name] = [item.unwrap() for item in value]
                else:
                    result[field_name] = value
            else:
                result[field_name] = value

        return result
