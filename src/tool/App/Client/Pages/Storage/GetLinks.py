from App.Client.Displayment import Displayment
from App import app

class GetLinks(Displayment):
    for_object = 'App.Objects.Operations.GetLinks'

    async def render_as_page(self, args = {}):
        query = self.request.rel_url.query
        storage = app.Storage.get(query.get('storage'))

        assert storage != None

        self.context.update({
            'storage': storage,
            'links': storage.adapter.getAllLinks()
        })

        return self.render_template('Storage/get_links.html')
