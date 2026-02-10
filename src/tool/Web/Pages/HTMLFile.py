from App.Objects.Object import Object
from App.Storage.StorageUnitLink import StorageUnitLink
from App.Storage.StorageUnit import StorageUnit
from pydantic import Field

class HTMLFile(Object):
    main: str = Field(default = 'index.html')
    assets: str = Field(default = 'assets')
    encoding: str = Field(default = 'utf-8')
    file: StorageUnitLink = Field(default = None)

    def create(self, storage_unit, link):
        self.file = StorageUnitLink(
            path = self.main,
            insertion = link.toInsert()
        )

        index_file = open(self.get_main(), 'w', encoding = self.encoding)
        index_file.close()

        storage_unit.get_root().joinpath(self.assets).mkdir(exist_ok = True)

        return self.file

    def get_main(self):
        return self.file.get_storage_unit().get_root().joinpath(self.main)

    def get_assets_dir(self):
        return self.file.get_storage_unit().get_root().joinpath(self.assets)

    def write(self, html: str):
        with open(self.get_main(), 'w', encoding = self.encoding) as file:
            file.write(html)
