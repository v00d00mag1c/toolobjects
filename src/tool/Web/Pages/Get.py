from App.Objects.Wheel import Wheel
from App.Objects.Object import Object
from App.Objects.Arguments.ArgumentDict import ArgumentDict
from App.Objects.Arguments.Argument import Argument
from App.Objects.Arguments.Assertions.NotNone import NotNone
from App.Objects.Arguments.AllowedValues import AllowedValues
from App.Objects.Relations.Submodule import Submodule
from Data.Types.Boolean import Boolean

class Get(Wheel):
    @classmethod
    def _submodules(cls) -> list:
        from Web.Pages.Downloader.FromHTML import FromHTML
        from Web.Pages.Downloader.ByURL import ByURL

        return [
            Submodule(
                item = ByURL,
                role = ['wheel']
            ),
            Submodule(
                item = FromHTML,
                role = ['wheel']
            )
        ]

    @classmethod
    def _arguments(cls) -> ArgumentDict:
        return ArgumentDict(items = [
            Argument(
                name = 'mode',
                orig = Object,
                default = 'Web.Pages.Crawler.Original',
                allowed_values = AllowedValues(
                    values = ['Web.Pages.Crawler.Original', 'Web.Pages.Crawler.Plain'],
                    strict = True
                )
            ),
            Argument(
                name = 'crawl',
                orig = Boolean,
                default = True
            )
        ],
        missing_args_inclusion=True)

    async def _implementation(self, i):
        extract = self._get_submodule(i)
        if extract == None:
            self._suitable_not_found_message()

            return await self._not_found_implementation(i)

        pages = await extract.execute(i)

        crawler = i.get('mode')
        do_crawl = i.get('crawl')
        for page in pages.getItems():
            if do_crawl:
                await crawler.process_page(page, i)

            page.clear()

        return 
