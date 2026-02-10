from App.Objects.Object import Object
from App.Storage.Item.StorageItem import StorageItem
from Web.Pages.HTMLFile import HTMLFile
from Web.Pages.Assets.Asset import Asset
from Web.Pages.Assets.Favicon import Favicon
from Web.Pages.Assets.Meta import Meta
from pydantic import Field

class Page(Object):
    html: HTMLFile = Field(default = None)
    assets: list[Asset] = Field(default = None)
    favicons: list[Favicon] = Field(default = [])
    meta_tags: list[Meta] = Field(default = [])
    page_links: list = Field(default = [])
    url: str = Field(default = None)
    base_url: str = Field(default = None)
    relative_url: str = Field(default = None)

    def set_title(self, title: str):
        self.obj.original_name = title

    def create_file(self, storage: StorageItem):
        storage_unit = storage.storage_adapter.get_storage_unit()
        self.link(storage_unit)

        self.html = HTMLFile()

        return self.html.create(storage_unit)

    def get_html_file(self):
        return self.file.get_storage_unit()
