from App.Client.Displayment import Displayment
from App.Client.Menu.Item import Item
from App import app
import aiohttp_jinja2

class Threads(Displayment):
    for_object = 'App.Objects.Threads.GetList'

    async def render_as_page(self):
        _list = list()
        for item in app.ThreadsList.getAll():
            _list.append(item)

        self.context.update({
            'tasks': _list
        })

        return self.render_template('App/threads.html')

    @classmethod
    def get_menu(cls) -> Item:
        return Item(
            url = cls.for_object,
            name = "client.task_manager",
            category_name = 'client.app'
        )
