from App.Client.Displayment import Displayment
from App.Objects.Index.ReloadAll import ReloadAll
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
                return aiohttp_jinja2.render_template('users/user.html', request, context)
            case _:
                return aiohttp_jinja2.render_template('app/management.html', request, context)

        return aiohttp.web.HTTPFound('/?i=App')
