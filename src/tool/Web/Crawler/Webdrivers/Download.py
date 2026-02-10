from App.Objects.Act import Act
from App.Objects.Object import Object
from App.Objects.Arguments.ArgumentDict import ArgumentDict
from App.Objects.Arguments.Argument import Argument
from App.Objects.Arguments.Assertions.NotNone import NotNone
from Data.Types.String import String
from App import app

class Download(Act):
    @classmethod
    def _arguments(cls) -> ArgumentDict:
        return ArgumentDict(items = [
            Argument(
                name = 'driver',
                orig = Object,
                default = 'Web.Crawler.Webdrivers.Chromedriver.Download',
                assertions = [NotNone()]
            )
        ], 
            missing_argument_inclusion = True
        )

    async def _implementation(self, i):
        _driver = i.get('driver')

        return await _driver().execute(i)
