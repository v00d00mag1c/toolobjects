from App.Client.Displayment import Displayment
from App.Client.Menu.Item import Item
from App import app
import aiohttp_jinja2

class Storages(Displayment):
    for_object = 'App.Storage.Item.List'

    async def render_as_page(self, request, context):
        query = request.rel_url.query

        context.update({
            'storages': app.Storage.items,
        })

        return aiohttp_jinja2.render_template('Storage/storages.html', request, context)

    @classmethod
    def get_menu(cls) -> Item:
        return Item(
            url = cls.for_object,
            name = "client.storages",
            category_name = 'client.index.content'
        )
