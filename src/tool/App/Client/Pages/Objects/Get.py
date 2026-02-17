from App.Client.Displayment import Displayment
from App import app
import aiohttp_jinja2

class Get(Displayment):
    for_object = 'App.Objects.Index.Get'

    async def render_as_page(self, args = {}):
        query = self.request.rel_url.query
        name = query.get('name')
        obj = app.ObjectsList.getByName(name)

        assert obj != None, 'not found object'

        do_load = query.get('load') == '1'
        mro_items = None

        if do_load or obj.is_inited:
            obj.loadModuleLater()

            mro_items = list()
            for item in obj.getModule().getMRO()[1:]:
                if hasattr(item, '_getNameJoined'):
                    mro_items.append(item)

        assert obj != None, 'object not found'

        self.context.update({
            'obj': obj,
            'False': False,
            'mro_items': mro_items,
            'displayment': self.get_for(name)
        })

        return self.render_template('Objects/object.html')
