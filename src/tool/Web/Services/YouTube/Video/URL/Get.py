from App.Objects.Extractor import Extractor
from App.Objects.Arguments.ArgumentDict import ArgumentDict
from App.Objects.Arguments.Argument import Argument
from App.Objects.Arguments.ListArgument import ListArgument
from App.Objects.Arguments.Assertions.NotNone import NotNone
from Data.Types.String import String
from Web.Services.YouTube.Video.URL.URL import URL
from urllib.parse import urlparse

class Get(Extractor):
    @classmethod
    def _arguments(cls) -> ArgumentDict:
        return ArgumentDict(items = [
            ListArgument(
                name = 'url',
                orig = String,
                assertions = [NotNone()]
            )
        ])

    async def _implementation(self, i):
        for url in i.get('url'):
            parsed = urlparse(url)

            new_url = URL()
            new_url.set_url(parsed)

            self.append(new_url)
