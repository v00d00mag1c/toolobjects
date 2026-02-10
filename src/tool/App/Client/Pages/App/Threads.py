from App.Client.Displayment import Displayment
from App.Client.Menu.Item import Item
from App import app
import aiohttp_jinja2

class Threads(Displayment):
    for_object = 'App.Objects.Threads.GetList'

    async def render_as_page(self, request, context):
        _list = list()
        for item in app.ThreadsList.getAll():
            _list.append(item)

        context.update({
            'tasks': _list
        })

        return aiohttp_jinja2.render_template('App/threads.html', request, context)

    @classmethod
    def get_menu(cls) -> Item:
        return Item(
            url = cls.for_object,
            name = "client.task_manager",
            category_name = 'client.app'
        )
