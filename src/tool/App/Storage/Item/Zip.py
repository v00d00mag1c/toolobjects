from App.Objects.Act import Act
from App.Storage.Item.StorageItem import StorageItem
from App.Objects.Arguments.Assertions.NotNone import NotNone
from App.Objects.Arguments.ArgumentDict import ArgumentDict
from App.Objects.Arguments.LiteralArgument import LiteralArgument
from App.Objects.Arguments.Argument import Argument
from Data.Types.Boolean import Boolean
from Data.Types.String import String
from App import app
import zipfile
import datetime
from pathlib import Path
from App.Objects.Responses.ObjectsList import ObjectsList
from Media.Files.FilePath import FilePath

class Zip(Act):
    '''
    Packs StorageItem to zip
    '''

    @classmethod
    def _arguments(cls) -> ArgumentDict:
        return ArgumentDict(items = [
            Argument(
                name = 'item',
                orig = StorageItem,
                assertions = [NotNone()]
            ),
            Argument(
                name = 'save_zip_to',
                orig = String,
                default = None
            ),
            Argument(
                name = 'name',
                orig = String,
                default = None
            ),
            Argument(
                name = 'zip_password',
                default = None,
                orig = String
            ),
            LiteralArgument(
                name = 'compression',
                values = ['ZIP_DEFLATED', 'ZIP_STORED', 'ZIP_BZIP2', 'ZIP_LZMA'],
                default = 'ZIP_DEFLATED',
            ),

        ])

    async def _implementation(self, i):
        storage = i.get('item')

        assert storage != None
        assert storage.has_storage_adapter()

        save_zip_to = i.get('save_zip_to')
        if save_zip_to == None:
            save_zip_to = app.app.storage
        else:
            save_zip_to = Path(save_zip_to)
        name = i.get("name")
        if name == None:
            name = f"{datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S')}.objects.zip"

        save_file_path = save_zip_to.joinpath(name)

        compression = None
        match(i.get('compression')):
            case "ZIP_DEFLATED":
                compression = zipfile.ZIP_DEFLATED
            case 'ZIP_STORED':
                compression = zipfile.ZIP_STORED
            case "ZIP_BZIP2":
                compression = zipfile.ZIP_BZIP2
            case "ZIP_LZMA":
                compression = zipfile.ZIP_LZMA

        zf = zipfile.ZipFile(save_file_path, "w", compression=compression)
        if i.get('zip_password') != None:
            zf.setpassword(bytes(i.get('zip_password')))

        with zf as zip_file:
            for file in storage.storage_adapter.get_all_files():
                zip_file.write(file, storage.storage_adapter.get_relative_path(file))

        zf.close()

        return ObjectsList(items = [FilePath(value = str(save_file_path))])
