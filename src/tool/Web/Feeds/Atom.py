from App.Objects.Object import Object
from Web.Feeds.Elements.Channel import Channel
from Web.Feeds.Elements.Entry import Entry
import xml.etree.ElementTree as ET

class Atom(Object):
    async def parse(self, data: ET):
        _channel = self._get_channel(data)
        print(len(data))

        for entry in data.findall('.//entry'):
            print(entry)
            _entry = self._get_entry(entry)
            print(_entry)

        return [_channel]

    def _get_channel(self, data: ET):
        channel = Channel()

        print(data.find('.//feed'))
        print(data.find('.//link'))
        for key in ['title', 'subtitle', 'id', 'link']:
            _val = data.find(key)
            print(_val)

            if _val != None:
                setattr(channel, key, _val.text)

        return channel

    def _get_entry(self, data: ET):
        entry = Entry()
        print(data)

        return entry
