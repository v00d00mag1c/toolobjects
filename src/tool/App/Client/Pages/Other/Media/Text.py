from App.Client.Displayment import Displayment
from Data.Types.String import String

class Text(Displayment):
    for_object = 'Media.Text.Text'

    async def render_as_object(self, item):
        self.context.update({
            'items': [item],
            'String': String,
        })

        return self.render_string('Other/Media/text_page.html')
