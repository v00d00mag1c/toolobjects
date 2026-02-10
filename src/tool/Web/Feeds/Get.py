from App.Objects.Extractor import Extractor
from Data.Types.String import String
from Web.Feeds.Elements.Feed import Feed
from App.Objects.Arguments.Assertions.NotNone import NotNone
from App.Objects.Arguments.ArgumentDict import ArgumentDict
from App.Objects.Arguments.Argument import Argument
from App.Objects.Misc.Source import Source
from Web.URL import URL
from App.Objects.Relations.Submodule import Submodule
from Web.Feeds.Elements.Channel import Channel
from Web.Feeds.Elements.Feed import Feed

from bs4 import BeautifulSoup


class Get(Extractor):
    @classmethod
    def _submodules(cls):
        return [
            Submodule(
                item = Channel,
                role = ['returns']
            )
        ]

    @classmethod
    def _arguments(cls) -> ArgumentDict:
        return ArgumentDict(items = [
            Argument(
                name = 'url',
                orig = String,
                assertions = [NotNone()]
            )
        ]).join_class(Feed)

    async def _implementation(self, i):
        url = i.get('url')
        self.log(f"downloading feed url: {url}")

        response_xml = await Feed.download(url)
        root = BeautifulSoup(response_xml, 'xml')
        _type = Feed.detect_type(root)

        assert _type != None, 'unknown type of feed'

        protocol = _type()
        channels = protocol._get_channels(root)

        for channel in channels:
            _new_time = None
            async for entry in protocol._get_entries(channel, root, i):
                if _new_time == None:
                    _new_time = entry.obj.created_at
                else: 
                    if entry.obj.created_at > _new_time:
                        _new_time = entry.obj.created_at

                entry.local_obj.make_public()
                channel.link(entry)

            channel.obj.set_common_source(Source(
                obj = URL(
                    value = url
                )
            ))
            channel.local_obj.updated_at = _new_time
            self.append(channel)
