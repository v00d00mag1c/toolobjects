from App.Objects.Act import Act
from App.Objects.Arguments.ArgumentDict import ArgumentDict
from App.Objects.Arguments.Argument import Argument
from Data.Types.Boolean import Boolean
from Data.Types.Int import Int
from Web.URL import URL
from Web.Feeds.Get import Get
from App import app

class Create(Act):
    @classmethod
    def _arguments(cls) -> ArgumentDict:
        return ArgumentDict(items = [
            Argument(
                name = 'url',
                orig = URL
            ),
            Argument(
                name = 'refresh_every',
                orig = Int,
                default = 120
            ),
            Argument(
                name = 'add_to_autostart',
                orig = Boolean,
                default = True
            )
        ],
        missing_args_inclusion=True)

    async def _implementation(self, i):
        url = i.get('url')
        add_to_autostart = i.get('add_to_autostart')
        save_to = i.get('save_to')
        refresh_every = i.get('refresh_every')

        assert save_to != ['tmp'], 'it must be saved somewhere'

        channels = await Get().execute({
            'url': url
        })
        channels.unsaveable = True
        autostart = app.Config.getItem().get('app.autostart.items', raw = True)

        # it will save channel in the first storageitem
        save_to_item = app.Storage.get(save_to[0])

        for channel in channels.getItems():
            channel.local_obj.make_public()
            channel.flush(save_to_item)
            channel.save()

            if add_to_autostart:
                _val = {
                    'unused': False,
                    'args': {
                        "i": "App.Objects.Operations.ExecuteIterative",
                        "i_2": "Web.Feeds.Update",
                        "interval": refresh_every,
                        "max_iterations": -1,
                        "channel": channel.getDbIds(),
                        "auth": "root"
                    }
                }

                await app.Autostart.run_by_dict(_val)
                autostart.append(_val)

            self.log('added channel {0} to autostart'.format(channel.getDbIds()))

        app.Config.getItem().set('app.autostart.items', autostart)

        return channels
