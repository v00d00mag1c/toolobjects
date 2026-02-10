from App.Objects.Object import Object
import xml.etree.ElementTree as ET

class RSS(Object):
    async def parse(self, data: ET):
        channels = list()

        for channel in data.findall('.//channel'):
            _channel = Channel.fromElement(channel)
            channels.append(_channel)

            for channel_item in channel.findall('.//item'):
                item = ChannelItem.fromElement(channel_item)
                if item.pubDate.timestamp() > self.last_time:
                    self.last_time = item.pubDate.timestamp()

                # _channel.link(item)
                self.append(item)

            if channel == None:
                _link = self.link(_channel)
                self.channel = _link.toInsert()

        return channels
