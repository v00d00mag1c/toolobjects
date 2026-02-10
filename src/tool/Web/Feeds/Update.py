from App.Objects.Act import Act
from App.Objects.Arguments.Assertions.NotNone import NotNone
from App.Objects.Arguments.ArgumentDict import ArgumentDict
from App.Objects.Arguments.Argument import Argument
from Web.Feeds.Elements.Channel import Channel
from Web.Feeds.Elements.Feed import Feed
import xml.etree.ElementTree as ET
from Web.Feeds.Elements.Feed import Feed

class Update(Act):
    @classmethod
    def _arguments(cls) -> ArgumentDict:
        return ArgumentDict(items = [
            Argument(
                name = 'channel',
                by_id = True,
                orig = Channel,
                assertions = [NotNone()]
            )
        ]).join_class(Feed)

    async def _implementation(self, i):
        _channel = i.get('channel')
        response_xml = await Feed.download(_channel.get_original_url())
        root = ET.fromstring(response_xml)
        _type = Feed.detect_type(root)

        assert _type != None, 'unknown type of feed'

        _count = 0
        _old_time = _channel.local_obj.updated_at
        _new_time = _old_time
        protocol = _type()

        async for entry in protocol._get_entries(_channel, root, i):
            # If found newer items
            if entry.obj.created_at > _old_time:
                entry.local_obj.make_public()
                if entry.obj.created_at > _new_time:
                    _new_time = entry.obj.created_at
                _channel.link(entry)

                _count += 1

        _channel.local_obj.updated_at = _new_time

        _channel.save()
        self.log('totally {0} new items; old time is {1}, new time is {2}'.format(_count, _old_time, _channel.local_obj.updated_at))
