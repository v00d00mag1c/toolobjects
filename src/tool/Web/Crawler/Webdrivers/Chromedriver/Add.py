from App.Objects.Act import Act
from App.Objects.Arguments.ArgumentDict import ArgumentDict
from App.Objects.Arguments.Argument import Argument
from App.Objects.Arguments.Assertions.NotNoneAssertion import NotNoneAssertion
from Data.String import String
from Web.Crawler.Webdrivers.Chromedriver.Chromedriver import Chromedriver
from App.Storage.StorageUnit import StorageUnit
from App.Objects.Responses.ObjectsList import ObjectsList
from App import app
import zipfile

class Add(Act):
    @classmethod
    def _arguments(cls) -> ArgumentDict:
        return ArgumentDict(items = [
            Argument(
                name = 'driver',
                orig = Chromedriver,
                default = None
            ),
            Argument(
                name = 'storage_unit',
                orig = StorageUnit,
                default = None
            ),
            Argument(
                name = 'driver_zip',
                orig = String,
                assertions = [NotNoneAssertion()]
            ),
            Argument(
                name = 'shell_zip',
                orig = String,
                assertions = [NotNoneAssertion()]
            ),
        ])

    async def implementation(self, i):
        bin = app.Storage.get('bin')

        driver = i.get('driver')
        storage_unit = i.get('storage_unit')

        driver_zip = i.get('driver_zip')
        shell_zip = i.get('shell_zip')

        if driver == None:
            driver = Chromedriver()
            driver.platform = Chromedriver._get_platform()

        if storage_unit == None:
            storage_unit = bin.storage_adapter.get_storage_unit()

        zip_driver_name = None
        root = storage_unit.get_root()
        driver_path = root.joinpath('driver')
        shell = root.joinpath('chrome')

        with zipfile.ZipFile(str(driver_zip), 'r') as zip_ref:
            _names = zip_ref.namelist()
            zip_driver_name = _names[0].split('/')[0]
            zip_ref.extractall(root)

        root.joinpath(zip_driver_name).rename(driver_path)

        with zipfile.ZipFile(str(shell_zip), 'r') as zip_ref:
            _names = zip_ref.namelist()
            shell_name = _names[0].split('/')[0]
            zip_ref.extractall(root)

        root.joinpath(shell_name).rename(shell)

        storage_unit.save()

        driver.file = driver.link(storage_unit).toInsert()
        driver.flush(bin)

        return ObjectsList(items = [driver], unsaveable = True)
