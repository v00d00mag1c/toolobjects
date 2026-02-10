from App.Client.Displayment import Displayment
from App import app
import aiohttp_jinja2

class ObjectsList(Displayment):
    for_object = 'App.Objects.Index.ObjectsList'

    async def render_as_page(self, args = {}):
        query = self.request.rel_url.query
        namespace_name = query.get('name')
        show_only = query.get('show_only')
        categories = dict()
        total_count = 0

        _items = None
        namespace = None
        if namespace_name:
            namespace = app.ObjectsList.get_namespace_with_name(namespace_name)
            _items = namespace.getItems()
        else:
            _items = app.ObjectsList.getItems().toList()

        categories, total_count = app.ObjectsList.sort(_items, show_only)

        self.context.update({
            'namespace': namespace,
            'categories': categories,
            'total_count': total_count,
            'hasattr': hasattr,
            'type': type
        })

        return self.render_template('Objects/objects_list.html')
