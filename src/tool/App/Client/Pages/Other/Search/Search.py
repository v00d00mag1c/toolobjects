from App.Client.Displayment import Displayment
from App import app
from App.Objects.Responses.ObjectsList import ObjectsList

class Search(Displayment):
    for_object = 'Data.Search'

    async def render_as_page(self, args = {}):
        query = self.request.rel_url.query

        _common = app.ObjectsList.get_namespace_with_name('common')
        if _common.is_loaded == False:
            _common.load_all()

        search_acts = list()
        for item in app.ObjectsList.getItems().iterate():
            try:
                if item.getModule().self_name == 'Search':
                    if item.get_name_for_dictlist() in ['Data.Search.Search']:
                        continue

                    search_acts.append(item.getModule())
            except Exception:
                pass

        self.context.update({
            'search_acts': search_acts,
        })

        if self.is_post():
            _checks = await self.request.post()
            q = _checks.get('q')
            checkmarks = []
            items = dict()

            for name, val in _checks.items():
                if name.startswith('check_') and val == 'on':
                    checkmarks.append(name[6:])

            for check in checkmarks:
                items[check] = await self._execute(check, {'q': q, 'as_result_items': True})

            self.context.update({
                'checkmarks': checkmarks,
                'items': items,
                'q': q
            })

        return self.render_template('Other/Search/search.html')
