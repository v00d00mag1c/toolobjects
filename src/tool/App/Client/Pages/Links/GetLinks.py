from App.Client.Displayment import Displayment
from App.Objects.Operations.GetLinks import GetLinks as RealGetLinks
import aiohttp_jinja2

class GetLinks(Displayment):
    for_object = 'App.Objects.Operations.GetLinks'

    async def render_as_page(self, args = {}):
        query = self.request.rel_url.query
        search_from = query.get('from')
        item = None

        self.context.update({
            'item': item
        })

        return self.render_template('Links/get_links.html')
