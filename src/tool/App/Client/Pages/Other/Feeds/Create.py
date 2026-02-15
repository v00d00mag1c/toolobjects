from App.Client.Displayment import Displayment
from App.Storage.Item.StorageItem import StorageItem

class Create(Displayment):
    for_object = 'Web.Feeds.Create'

    async def render_as_page(self, args = {}):
        query = self.request.rel_url.query
        item = self.get_link_item()

        assert item != None

        self.context.update({
            'item': item,
            'args': args,
        })

        if self.is_post():
            data = await self.request.post()
            url = data.get('url')

            _storage = None
            if item.isInstance(StorageItem):
                _storage = item.name
            else:
                _storage = item.getDbName()

            assert url != '', 'url = null'

            refresh_every = data.get('refresh_every', None)
            new_items = await self._execute('Web.Feeds.Create', {
                'url': url,
                'refresh_every': refresh_every,
                'save_to': [_storage]
            })
            new_item = new_items.items[0]

            self._flush_creation(item, new_item)

            return self.redirect('/?i=App.Objects.Object&uuids=' + new_item.getDbIds())

        return self.render_template('Other/Feeds/create.html')
