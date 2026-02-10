from App.Objects.Object import Object
from App.Storage.StorageUnitLink import StorageUnitLink
from App.Storage.StorageUnit import StorageUnit
from App.Storage.Item.StorageItem import StorageItem
from Web.Pages.HTMLFile import HTMLFile
from Web.Pages.Assets.Favicon import Favicon
from pydantic import Field

class Page(Object):
    html: HTMLFile = Field(default = None)
    favicons: list[Favicon] = Field(default = [])
    url: str = Field(default = None)
    base_url: str = Field(default = None)
    relative_url: str = Field(default = None)

    def set_title(self, title: str):
        self.obj.original_name = title

    def create_file(self, storage: StorageItem):
        self.html = HTMLFile()
        return self.html.create(storage)

    def get_html_file(self):
        return self.file.get_storage_unit()
