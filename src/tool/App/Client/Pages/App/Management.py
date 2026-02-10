from App.Client.Displayment import Displayment
from App.Objects.Index.ReloadAll import ReloadAll
from App.Client.Menu.Item import Item
from App.Locale.Reload import Reload
from App import app
import aiohttp_jinja2
import aiohttp

class Management(Displayment):
    for_object = 'App'

    async def render_as_page(self, request, context):
        query = request.rel_url.query
        act = query.get('act')

        match(act):
            case 'reload_modules':
                await ReloadAll().execute()
            case 'reload_locales':
                await Reload().execute()
            case 'turn_off':
                exit(-1)
            case 'self_user':
                return aiohttp_jinja2.render_template('Users/user.html', request, context)
            case 'displayments':
                context.update({
                    'displayments': app.app.view.displayments.items()
                })
                return aiohttp_jinja2.render_template('App/displayments.html', request, context)
            case _:
                return aiohttp_jinja2.render_template('App/management.html', request, context)

        return aiohttp.web.HTTPFound('/?i=App')

    @classmethod
    def get_menu(cls) -> Item:
        return Item(
            url = cls.for_object,
            name = "client.management",
            category_name = 'client.app'
        )
