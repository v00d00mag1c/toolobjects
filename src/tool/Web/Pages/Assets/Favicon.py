from Web.Pages.Assets.Asset import Asset
from App.Objects.Object import Object
from pydantic import Field
from typing import Optional
from App import app

class Favicon(Object, Asset):
    url: str = Field(default = None)
    sizes: Optional[str] = Field(default = None)

    async def download_function(self, dir):
        _item = app.DownloadManager.addURL(self.url, dir, self.get_encoded_url())
        await _item.start()

    def replace(self):
        _node = self.get_node()

        if _node != None and _node.get('href'):
            _node['data-tobj.orig'] = self.url
            _node['href'] = self.get_encoded_url()

    def set_url(self, href: str, base_url: str = ''):
        if not href.startswith('http'):
            href = base_url + href

        self.url = href

    def get_url(self):
        return self.url
