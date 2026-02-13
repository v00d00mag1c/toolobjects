from App.Client.Displayment import Displayment
from App import app
import aiohttp_jinja2

class Object(Displayment):
    for_object = 'App.Objects.Object'

    async def render_as_page(self, args = {}):
        query = self.request.rel_url.query
        act = query.get('act')
        redirect_if_no_displayment = query.get('redirect_if_no_displayment') == 'on'
        objs = self.get_objs(query.get('uuids', '').split(','))

        assert len(objs) > 0, 'objects not found'

        self.context.update({
            'objects': objs,
            'ref': query.get('ref')
        })

        match(act):
            case 'view_json':
                include_nones = query.get('include_none') == '1'
                _json = list()
                for item in objs:
                    _json.append(item.to_json(exclude_none = include_nones, exclude_defaults = include_nones))

                return self.return_json(_json)
            case 'display':
                _as = query.get('as')
                htmls = list()
                for item in objs:
                    _class = self.get_for(_as)
                    if _class == None:
                        if redirect_if_no_displayment:
                            return self.redirect_to_object(item)
                        else:
                            htmls.append(
                                (item, aiohttp_jinja2.render_string('Components/message.html', self.request, {'message': 'not found displayment for ' + _as}))
                            )
                        continue
                    else:
                        displayment = _class()
                        displayment.request = self.request
                        displayment.context = self.context

                        if displayment.prefer_object_displayment == 'object':
                            htmls.append((item, await displayment.render_as_object(item)))
                        else:
                            return await displayment.render_as_page({
                                'item': item
                            })

                self.context['htmls'] = htmls

                return self.render_template('Objects/displayments.html')
            case 'show_thumbnails':
                thumbs = list()
                for item in objs:
                    for thumb in item.get_thumbnails():
                        thumbs.append(thumb)

                self.context.update({
                    'thumbnails': thumbs,
                    'ref': query.get('ref')
                })
                return self.render_template('Objects/thumbnails.html')

        return self.render_template('Objects/db_object.html')

    async def render_as_list_item(self, item, args):
        self.context.update({
            'item': item,
            'args': args,
            'object_show_id': args.get('object_show_id', True)
        })
        return self.render_string('Objects/object_listview.html')

    async def render_as_collection(self, orig_items, args, orig_collection = None):
        # getting html for each item

        html_items = list()
        for item in orig_items:
            try:
                _d = self.get_for(args.get('display_as'))(request = self.request, context = self.context)
                _html = await _d.render_as_list_item(item, {'object_show_id': False})

                html_items.append([item, _html])
            except Exception as e:
                self.log_error(e)
                html_items.append([item, '<div><b class="error">{0}</b></div>'.format(str(e))])

        self.context.update({
            'items': html_items,
            'args': args
        })
        return self.render_string('Explorer/objects_list.html')
