from App.Client.Displayment import Displayment
from App.Client.Menu.Item import Item
from App import app
import aiohttp_jinja2

class Namespaces(Displayment):
    for_object = 'App.Objects.Index.GetList'

    async def render_as_page(self, args = {}):
        items = None

        self.context.update({
            'namespaces': app.ObjectsList.namespaces,
            'objects': items
        })

        return self.render_template('Objects/namespaces.html')

    @classmethod
    def get_menu(cls) -> Item:
        return Item(
            url = cls.for_object,
            name = "client.namespaces",
            category_name = 'client.index.content'
        )
