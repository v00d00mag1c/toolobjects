from App.Client.Displayment import Displayment
from Data.Types.String import String

class Image(Displayment):
    for_object = 'Media.Images.Image'

    async def render_as_object(self, item):
        self.context.update({
            'items': [item],
        })

        return self.render_string('Other/Media/image.html')
