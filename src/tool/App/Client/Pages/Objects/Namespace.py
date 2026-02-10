from App.Client.Displayment import Displayment
from App import app
import aiohttp_jinja2

class Namespace(Displayment):
    for_object = 'App.Objects.Index.Namespaces.Get'

    async def render_as_page(self):
        query = self.request.rel_url.query
        namespace = app.ObjectsList.get_namespace_with_name(query.get('name'))

        assert namespace != None, 'not found namespace'

        self.context.update({
            'namespace': namespace
        })

        return self.render_template('Objects/namespace.html')
