from App.Client.Displayment import Displayment

class CreateYouTubeURL(Displayment):
    for_object = ['Web.Services.YouTube.Video.URL.Get']

    async def render_as_page(self, args = {}):
        orig_item = self.get_link_item()

        assert orig_item != None

        self.context.update({
            'item': orig_item,
            'args': args,
        })

        if self.is_post():
            data = await self.request.post()
            items = await self._execute(self.for_object[0], {
                'url': data.get('youtube_url')
            })

            return self.redirect(self._flush_creation(orig_item, items.get(0)))

        return self.render_template('Other/Web/Services/create_youtube_url.html')
