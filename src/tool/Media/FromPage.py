from App.Objects.Extractor import Extractor
from App.Objects.Object import Object
from App.Objects.Arguments.ArgumentDict import ArgumentDict
from App.Objects.Arguments.Assertions.NotNone import NotNone
from App.Objects.Arguments.Argument import Argument
from App.Objects.Arguments.ListArgument import ListArgument
from App.Objects.Responses.ObjectsList import ObjectsList
from Data.Types.String import String
from Web.Pages.Page import Page

class FromPage(Extractor):
    @classmethod
    def _arguments(cls) -> ArgumentDict:
        return ArgumentDict(items = [
            Argument(
                name = 'object',
                orig = Object,
                assertions = [NotNone()]
            ),
            ListArgument(
                name = 'page',
                orig = Page,
                by_id = True,
                assertions = [NotNone()]
            ),
            ListArgument(
                name = 'selector',
                orig = String,
            )
        ],
        missing_args_inclusion=True)

    async def _implementation(self, i):
        objs = ObjectsList(items = [])
        for page in i.get('page'):
            html = page.get_html()
            if html == None:
                self.log('page {0} does not contains html'.format(html.getDbIds()))

                continue

        return objs
