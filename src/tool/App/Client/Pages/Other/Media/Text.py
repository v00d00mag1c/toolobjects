from App.Client.Displayment import Displayment
from Data.Types.String import String

class Text(Displayment):
    for_object = 'Media.Text.Text'

    async def render_as_object(self, item):
        query = self.request.rel_url.query
        self.context.update({
            'items': [item],
            'sub_act': query.get('sub_act'),
            'String': String,
        })

        if self.is_post():
            data = await self.request.post()
            ignore_escaping = data.get('ignore_escaping') == 'on'
            self.context.update({
                'ignore_escaping': ignore_escaping,
                'sub_act': data.get('sub_act')
            })

        return self.render_string('Other/Media/text_page.html')

    async def render_as_edit(self, item, args = {}):
        query = self.request.rel_url.query
        item = self._get_item()

        assert item != None
        self.context.update({
            'ref': query.get('ref'),
            'db_item': item
        })

        if self.is_post():
            data = await self.request.post()
            new_text = data.get('text')

            assert new_text != None

            item.value = new_text
            item.save()

            return self.redirect_to_object(item, as_self = True)

        return self.render_template('Other/Media/text.html')
