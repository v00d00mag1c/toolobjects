from App.Client.Displayment import Displayment
from App import app
import aiohttp_jinja2

class Namespace(Displayment):
    for_object = 'App.Objects.Index.Namespaces.Get'

    async def render_as_page(self, args = {}):
        query = self.request.rel_url.query
        act = query.get('act')
        namespace = app.ObjectsList.get_namespace_with_name(query.get('name'))

        match(act):
            case 'load_all':
                if namespace:
                    for item in namespace.getItems():
                        try:
                            item.getModule()
                        except Exception:
                            pass

                    return self.redirect('/?i=App.Objects.Index.Namespaces.Get&name=' + namespace.name)

        _items = None
        if namespace:
            _items = namespace.getItems()
        else:
            _items = app.ObjectsList.getItems().toList()

        categories, total_count = app.ObjectsList.sort(_items)

        self.context.update({
            'namespace': namespace,
            'categories': categories,
            'hasattr': hasattr,
            'total_count': total_count
        })

        return self.render_template('Objects/namespace.html')
