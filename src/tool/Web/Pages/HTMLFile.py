from App.Objects.Object import Object
from App.Storage.StorageUnitLink import StorageUnitLink
from App.Storage.StorageUnit import StorageUnit
from pydantic import Field

class HTMLFile(Object):
    main: str = Field(default = 'index.html')
    encoding: str = Field(default = 'utf-8')
    file: StorageUnitLink = Field(default = None)

    def create(self, storage):
        _unit = storage.storage_adapter.get_storage_unit()

        self.file = StorageUnitLink(
            path = self.main,
            insertion = self.link(_unit).toInsert()
        )

        index_file = open(self.get_main(), 'w', encoding = self.encoding)
        index_file.close()

        return _unit

    def get_main(self):
        return self.file.get_storage_unit().get_root().joinpath(self.main)

    def write(self, html: str):
        with open(self.get_main(), 'w', encoding = self.encoding) as file:
            file.write(html)
