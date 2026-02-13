from App.Client.Displayment import Displayment
from App.Objects.Index.ReloadAll import ReloadAll
from App.Client.Menu.Item import Item
from App.Locale.Reload import Reload
from App import app
import aiohttp_jinja2
import aiohttp

class Management(Displayment):
    for_object = 'App'

    async def render_as_page(self, args = {}):
        query = self.request.rel_url.query
        response = aiohttp.web.HTTPFound('/?i=App')
        act = query.get('act')

        match(act):
            case 'reload_modules':
                await ReloadAll().execute()
            case 'reload_locales':
                await Reload().execute()
            case 'turn_off':
                exit(-1)
            case 'self_user':
                return self.render_template('Users/user.html')
            case 'displayments':
                self.context.update({
                    'displayments': app.app.view.displayments.items()
                })
                return self.render_template('App/displayments.html')
            case 'change_theme':
                if self.request.cookies.get('theme') == 'dark_theme':
                    response.set_cookie('theme', '')
                else:
                    response.set_cookie('theme', 'dark_theme')
            case _:
                return self.render_template('App/management.html')

        return response

    @classmethod
    def get_menu(cls) -> Item:
        return Item(
            url = cls.for_object,
            name = "client.management",
            category_name = 'client.app'
        )
