from App.Objects.Object import Object
from App.Storage.StorageUnitLink import StorageUnitLink
from App.Storage.StorageUnit import StorageUnit
from Web.Pages.Assets.Asset import Asset
from pydantic import Field
import chardet

class HTMLFile(Object):
    main: str = Field(default = 'index.html')
    assets: str = Field(default = 'assets')
    encoding: str = Field(default = 'utf-8')
    file: StorageUnitLink = Field(default = None)
    assets_links: dict = Field(default = {})

    def set_encoding(self, val: str):
        self.log('set encoding to {0}'.format(val))

        self.encoding = val

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
        return self._get('file').get_storage_unit().get_root().joinpath(self.main)

    def get_assets_dir(self):
        _path = self._get('file').get_storage_unit().get_root().joinpath(self.assets)
        _path.mkdir(exist_ok = True)
        return _path

    def get_asset_by_url(self, url: str):
        asset = None
        for attempt in range(0, 3):
            match (attempt):
                case 0:
                    asset = self.assets_links.get(Asset.encode_url(url))
                case 1:
                    asset = self.assets_links.get(Asset.encode_url(url.strip()))
                case 2:
                    asset = self.assets_links.get(url.replace('https', 'http', 1))

            if asset != None:
                return asset

        return asset

    def write(self, html: str):
        _detect = chardet.detect(html.encode('utf-8', errors='ignore'))

        self.set_encoding(_detect.get('encoding'))

        try:
            with open(self.get_main(), 'w', encoding = self.encoding) as file:
                file.write(html)
        except Exception as e:
            self.log_error(e, exception_prefix = "Error when writing file, encoding is {0}, trying UTF-8. ".format(self.encoding))

            with open(self.get_main(), 'w', encoding = 'utf-8') as file:
                file.write(html)
