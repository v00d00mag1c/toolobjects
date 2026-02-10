from Web.Pages.Assets.Asset import Asset
from pydantic import Field
from App import app

class Favicon(Asset):
    url: str = Field(default = None)
    sizes: str = Field()

    async def download_function(self, dir):
        app.DownloadManager.addURL(self.url)

    def set_url(self, href: str, base_url: str = ''):
        if not href.startswith('http'):
            href = base_url + href

        self.url = href
