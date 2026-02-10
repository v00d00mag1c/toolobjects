from App.Objects.Act import Act
from App.Objects.Arguments.Argument import Argument
from App.Objects.Arguments.Assertions.NotNone import NotNone
from App.Objects.Arguments.ArgumentDict import ArgumentDict
from Web.Pages.Crawler.Webdrivers.Chromedriver.Chromedriver import Chromedriver
from Data.Types.String import String
from App import app

class Create(Act):
    # Creates webdriver with some executable_path

    @classmethod
    def _arguments(cls) -> ArgumentDict:
        return ArgumentDict(items = [
            Argument(
                name = 'executable_path',
                orig = String,
                assertions = [NotNone()]
            )
        ])

    async def _implementation(self, i):
        _bin = app.Storage.get('bin')

        _new = Chromedriver()
        _new.executable_path = i.get('executable_path')

        _bin.flush(_new)
