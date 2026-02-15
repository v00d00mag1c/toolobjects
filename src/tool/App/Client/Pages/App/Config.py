from App.Client.Displayment import Displayment
from App.Client.Menu.Item import Item
from App import app
import json

class Config(Displayment):
    for_object = 'App.Config'

    @classmethod
    def get_menu(cls) -> Item:
        return None
        return Item(
            url = cls.for_object,
            name = "client.config",
            category_name = 'client.app'
        )

    async def render_as_page(self, args = {}):
        query = self.request.rel_url.query
        act = query.get('act')
        keys = app.Config.getItem().values.compare.toDict()

        self.context.update({
            'keys': keys,
            'act': act
        })

        match (act):
            case 'edit':
                key = query.get('key')
                val = None
                _val = None

                try:
                    _val = app.Config.getItem().get(key, raw = True)

                    if type(_val) == list:
                        val = json.dumps(_val, indent = 4, ensure_ascii = False)
                    else:
                        if type(_val) == bool:
                            val = int(_val)
                        else:
                            val = _val
                except:
                    pass

                if val == None:
                    val = ''

                self.context.update({
                    'key': key,
                    'val': val
                })

                if self.is_post():
                    data = await self.request.post()
                    app.Config.getItem().set(key, data.get('config_value'), save_old_values = True)
                    return self.redirect('/?i=App.Config')

        return self.render_template('App/config.html')
