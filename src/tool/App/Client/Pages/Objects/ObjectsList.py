from App.Client.Displayment import Displayment
from App import app
import aiohttp_jinja2

class ObjectsList(Displayment):
    for_object = 'App.Objects.Index.ObjectsList'

    async def render_as_page(self, request, context):
        query = request.rel_url.query
        namespace_name = query.get('name')
        namespace = None
        categories = dict()
        total_count = 0

        if namespace_name:
            namespace = app.ObjectsList.get_namespace_with_name(namespace_name)
            categories, total_count = app.ObjectsList.sort(namespace.getItems())
        else:
            categories, total_count = app.ObjectsList.sort(app.ObjectsList.getItems().toList())

        context.update({
            'namespace': namespace,
            'categories': categories,
            'total_count': total_count,
            'hasattr': hasattr,
            'type': type
        })

        return aiohttp_jinja2.render_template('Objects/objects_list.html', request, context)
