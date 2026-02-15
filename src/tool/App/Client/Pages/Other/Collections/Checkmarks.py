from App.Client.Displayment import Displayment

class Checkmarks(Displayment):
    for_object = 'Data.Primitives.Checkmarks.List'
    prefer_object_displayment = 'page'

    async def render_as_page(self, args = {}):
        query = self.request.rel_url.query
        items = self.get_objs(query.get('uuids').split(','))

        self.context.update({
            'items': items,
            'ref': query.get('ref')
        })

        if self.is_post():
            data = await self.request.post()
            act = data.get('act')

            match (act):
                case 'add_checkmark':
                    obj_id = self.get_objs(data.get('uuid').split(','))[0]
                    new_items = await self._execute('Data.Primitives.Checkmarks.AddCheckmark', {
                        'list': data.get('uuid'),
                        'label': data.get('todolist_new_task_name')
                    })

        return self.render_template('Other/Collections/checkmarks.html')
