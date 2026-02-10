from App.Client.Displayment import Displayment
from App import app

class StopTask(Displayment):
    for_object = 'App.Objects.Threads.Stop'

    async def render_as_page(self):
        ids = int(self.request.rel_url.query.get('id'))
        task = app.ThreadsList.getById(ids)

        assert task != None, 'task not exists'

        task.end()

        return self.redirect('/?i=App.Objects.Threads.GetList')
