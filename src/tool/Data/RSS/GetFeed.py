from App.Objects.Extractor import Extractor
from App.Objects.Misc.LinkInsertion import LinkInsertion
from Data.String import String
from App.Responses.ObjectsList import ObjectsList
from Data.RSS.Channel import Channel
from Data.RSS.ChannelItem import ChannelItem
from pydantic import Field
from typing import Optional, Self
import datetime
import xml.etree.ElementTree as ET
from App.Objects.Arguments.Assertions.NotNoneAssertion import NotNoneAssertion
from App.Objects.Arguments.ArgumentDict import ArgumentDict
from App.Objects.Arguments.Argument import Argument
from Data.RSS.Response import Response

# Should it be in Web category or in Data? i dont know
class GetFeed(Extractor):
    channel: Optional[Channel | LinkInsertion] = Field(default = None)
    last_time: float = Field(default = 0)

    @classmethod
    def getArguments(cls) -> ArgumentDict:
        return ArgumentDict(items = [
            Argument(
                name = 'url',
                orig = String,
                assertions = [NotNoneAssertion()]
            )
        ])

    async def implementation(self, i):
        url = i.get('url')
        response_xml = await Response.download(url)

        self.log(f"downloaded url: {url}")

        root = ET.fromstring(response_xml)
        channels = list()

        for channel in root.findall('.//channel'):
            _channel = Channel.fromElement(channel)
            channels.append(_channel)

            for channel_item in channel.findall('.//item'):
                item = ChannelItem.fromElement(channel_item)
                if item.pubDate.timestamp() > self.last_time:
                    self.last_time = item.pubDate.timestamp()

                # _channel.link(item)
                self.append(item)

            if self.channel == None:
                _link = self.link(_channel)
                self.channel = _link.toInsert()

    async def update(self, old: Self, response: ObjectsList) -> ObjectsList:
        _new = ObjectsList()

        self.log(f'old last time is {old.last_time}')
        for item in response.getItems():
            if item.pubDate.timestamp() > old.last_time:
                _new.append(item)

        self.log_diff(_new.getCount())

        return _new
