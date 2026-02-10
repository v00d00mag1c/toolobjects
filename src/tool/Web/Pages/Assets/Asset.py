from App.Objects.Mixins.BaseModel import BaseModel
from App.Storage.StorageUnit import StorageUnit
from abc import abstractmethod
from pydantic import Field
from typing import Any
import secrets
import urllib

class Asset(BaseModel):
    bs_node: Any = Field(default = None)
    _unserializable = ['bs_node']

    async def download(self, dir: str):
        await self.download_function(dir)

    @abstractmethod
    async def download_function(self, dir: str):
        pass

    def get_encoded_url(self):
        return urllib.parse.quote(self.url).replace('/', '%')

    def set_node(self, bs_node):
        self.bs_node = bs_node

    def get_node(self):
        return self.bs_node
