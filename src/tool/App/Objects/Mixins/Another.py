from pydantic import computed_field
from App.Objects.Mixins.Model import Model

class Another():
    def _get_name(self) -> str:
        return self._getNameJoined()

    def get_width(self) -> float:
        if self.obj.width:
            return self.obj.width

        if self.local_obj.width:
            return self.local_obj.width

        return 500

    def get_height(self) -> float:
        if self.obj.height:
            return self.obj.height

        if self.local_obj.height:
            return self.local_obj.height

        return 300

    def add_thumbnail(self, item: Model):
        self.link(item, role = ['thumbnail'])

    def add_thumbnails(self, items):
        for item in items:
            self.add_thumbnail(item)

    def get_thumbnails(self, include_linked: bool = True):
        '''
        Returns image thumbnails links (not objects)
        '''
        #for thumb in self.local_obj.thumbnail:
        #    thumb.setDb(self.getDb())

        #    yield thumb

        for thumb in self.getLinked(with_role = 'thumbnail'):
            yield thumb

    def get_image_thumbnail(self):
        items = list()
        for link in self.get_thumbnails():
            if hasattr(link.item, 'media_type') and link.item.media_type in ['image']:
                items.append(link)

        return items

    def has_image_thumbnail(self):
        _res = self.get_image_thumbnail()

        return len(_res) > 0

    @computed_field
    @property
    def any_name(self) -> str:
        if self.local_obj.name:
            return self.local_obj.name
        if self.obj.name:
            return self.obj.name

        return self._get_name()

    @computed_field
    @property
    def any_description(self) -> str:
        if self.local_obj.description:
            return self.local_obj.description
        if self.obj.description:
            return self.obj.description

        return ''

    def has_description(self) -> bool:
        return len(self.any_description) > 0
