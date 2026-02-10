from App.Client.Displayment import Displayment
from App.Storage.VirtualPath.Navigate import Navigate
from App.Storage.VirtualPath.Path import Path as VirtualPath
import aiohttp_jinja2
import aiohttp

class Explorer(Displayment):
    for_object = 'App.Storage.VirtualPath.Navigate'

    async def render_as_page(self, args = {}):
        query = self.request.rel_url.query
        path_val = query.get('path')

        if path_val == '':
            return aiohttp.web.HTTPFound('/?i=App.Storage.Item.List')

        try:
            path = VirtualPath.from_str(path_val)
        except IndexError as e:
            self.log_error(e)

        self.context.update({
            'path': path,
            'items': await Navigate().execute({
                'path': path,
                'count': 30,
                'limit': 100
            }),
        })

        return self.render_template('Explorer/virtual_path.html')
