from App.Client.Displayment import Displayment
from App.Client.Menu.Item import Item
from App import app
import aiohttp_jinja2

class Storages(Displayment):
    for_object = 'App.Storage.Item.List'

    async def render_as_page(self):
        query = self.request.rel_url.query
        show_internal = query.get('show_internal') == 'on'

        items = list()
        for item in app.Storage.items:
            if show_internal is False:
                if item.is_internal:
                    continue

            items.append(item)

        self.context.update({
            'storages': items,
            'show_internal': show_internal
        })

        return self.render_template('Storage/storages.html')

    @classmethod
    def get_menu(cls) -> Item:
        return Item(
            url = cls.for_object,
            name = "client.storages",
            category_name = 'client.index.content'
        )
