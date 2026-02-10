from App.Objects.Extractor import Extractor
from App.Objects.Arguments.ArgumentDict import ArgumentDict
from App.Objects.Arguments.Argument import Argument
from Data.String import String
from App.Objects.Arguments.Assertions.NotNoneAssertion import NotNoneAssertion
from App.Responses.ObjectsList import ObjectsList
from Data.RSS.Channel import Channel
from Data.RSS.ChannelItem import ChannelItem
from pydantic import Field
from typing import Optional
import datetime

# Should it be in Web category or in Data? i dont know
class GetFeed(Extractor):
    channel: Optional[Channel] = Field(default = None)
    last_time: datetime.datetime = Field(default = 0)

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
        import aiohttp, xmltodict

        url = i.get('url')
        response_xml = None

        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                response_xml = await response.text()

        self.log(f"url: {url}")
        rss_response = xmltodict.parse(response_xml)
        rss = rss_response.get('rss')
        _channel = rss.get('channel')
        self.channel = Channel(
            title = _channel.get('title'),
            description = _channel.get('description'),
            channel_link = _channel.get('link'),
            generator = _channel.get('generator'),
            copyright = _channel.get('copyright'),
            language = _channel.get('language'),
        )
        self.link(self.channel)

        for item in _channel.get('item'):
            channel_item = self.channel.addItem(item)
            if channel_item.pubDate.timestamp() > self.last_time:
                self.last_time = channel_item.pubDate

            self.channel.link(channel_item)
            self.append(channel_item)

    async def update(self, response: ObjectsList) -> ObjectsList:
        _new = ObjectsList()
        for item in response.getItems():
            _new.append(item)

        return _new
