from App.Client.Displayment import Displayment
from App.Objects.Operations.Edit import Edit as RealEdit
from App.Objects.Operations.Edit.NewJSON import NewJSON
from Data.Types.JSON import JSON

class EditFields(Displayment):
    for_object = ['App.Objects.Operations.Edit', 'App.Objects.Operations.Edit.Edit']

    async def render_as_page(self, args = {}):
        query = self.request.rel_url.query
        path_val = query.get('item')
        act = query.get('act')

        item = self.get_objs([path_val])[0]

        assert item != None, 'not found'
        assert act in ['json', None], 'wrong act'
        assert item.isEditable(), 'access denied'

        match(act):
            case 'json':
                _json = JSON(data = item.to_db_json(exclude_output_values = item._unserializable_on_output))
                self.context.update({
                    'json': _json.dump(4)
                })

        self.context.update({
            'item': item,
            'act': act
        })

        if self.is_post():
            data = await self.request.post()

            try:
                match(act):
                    case None:
                        pass
                    case 'json':
                        _json = data.get('json')
                        await NewJSON().execute({
                            'item': item,
                            'json': _json
                        })

                        return self.redirect_to_object(item)
            except Exception as e:
                self.throw_message(str(e))
                self.log_error(e)

        return self.render_template("Actions/edit_fields.html")
