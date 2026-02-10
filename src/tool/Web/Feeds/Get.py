from App.Objects.Extractor import Extractor
from Data.String import String
from Web.Feeds.Elements.Feed import Feed
from App.Objects.Arguments.Assertions.NotNone import NotNone
from App.Objects.Arguments.ArgumentDict import ArgumentDict
from App.Objects.Arguments.Argument import Argument

from App.Objects.Responses.ObjectsList import ObjectsList

import xml.etree.ElementTree as ET

class Get(Extractor):
    @classmethod
    def _arguments(cls) -> ArgumentDict:
        return ArgumentDict(items = [
            Argument(
                name = 'url',
                orig = String,
                assertions = [NotNone()]
            )
        ])

    async def _implementation(self, i):
        url = i.get('url')
        self.log(f"downloading feed url: {url}")

        response_xml = await Feed.download(url)
        root = ET.fromstring(response_xml)
        _type = Feed.detect_type(root)

        assert _type != None, 'unknown type of feed'

        channels = await _type().parse(root)

        return ObjectsList(items = channels)
