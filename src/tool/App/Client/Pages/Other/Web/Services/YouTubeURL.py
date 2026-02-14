from App.Client.Displayment import Displayment

class YouTubeURL(Displayment):
    for_object = 'Web.Services.YouTube.Video.URL.URL'

    async def render_as_object(self, item):
        self.context.update({
            'items': [item],
        })

        return self.render_string('Other/Web/Services/youtube_url.html')
