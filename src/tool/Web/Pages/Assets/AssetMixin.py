from App.Objects.Mixins.BaseModel import BaseModel
from App.Storage.StorageUnit import StorageUnit
from abc import abstractmethod
from pydantic import Field
from typing import Any
from App import app
import secrets
import urllib

class AssetMixin(BaseModel):
    url: str = Field(default = None)
    bs_node: Any = Field(default = None)
    _unserializable = ['bs_node']

    # we know that contents are downloaded so it will available in the displayment
    def replace(self):
        _node = self.get_node()

        if _node != None and (_node.get('href') or _node.get('src')):
            _node['data-__to_orig'] = self.url
            _key = 'href'

            if _node.get('src') != None and _node.get('src') != '':
                _key = 'src'

            _node['data-__to_orig_key'] = _key
            _node[_key] = ''

    def decompose(self):
        self.bs_node.decompose()

    def set_url(self, href: str, base_url: str = ''):
        if not href.startswith('http'):
            href = base_url + href

        self.url = href

    def get_url(self):
        return self.url

    def has_url(self):
        return self.url != None

    async def download(self, dir: str):
        await self.download_function(dir)

    async def download_function(self, dir):
        _item = app.DownloadManager.addURL(self.url, dir, self.get_encoded_url())
        await _item.start()

    def get_encoded_url(self):
        return urllib.parse.quote(self.url).replace('/', '%')

    @staticmethod
    def get_decoded_url(url):
        return urllib.parse.unquote(url).replace('%', '/')

    @staticmethod
    def encode_url(url):
        return urllib.parse.quote(url).replace('/', '%')

    def set_node(self, bs_node):
        self.bs_node = bs_node

    def get_node(self):
        return self.bs_node
