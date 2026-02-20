from App.Objects.Act import Act
from App.Objects.Arguments.Argument import Argument
from App.Objects.Arguments.Assertions.NotNone import NotNone
from App.Objects.Arguments.ArgumentDict import ArgumentDict
from Web.Pages.Crawler.Webdrivers.Chromedriver.Chromedriver import Chromedriver
from Data.Types.String import String
from Data.Types.Boolean import Boolean
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
            ),
            Argument(
                name = 'user_data_dir',
                orig = String,
                default = None
            ),
            Argument(
                name = 'set_as_current',
                orig = Boolean,
                default = False
            )
        ])

    async def _implementation(self, i):
        user_data_dir = i.get('user_data_dir')
        _bin = app.Storage.get('bin')

        _new = Chromedriver()
        _new.executable_path = i.get('executable_path')
        if user_data_dir != None:
            _new.user_data_dir = user_data_dir

        _bin.flush(_new)

        _new.save()

        if i.get('set_as_current'):
            app.Config.set("web.crawler.webdriver", _new.getDbIds())
