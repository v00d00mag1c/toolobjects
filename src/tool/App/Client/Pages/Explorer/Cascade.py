from App.Client.Displayment import Displayment
from App.Objects.Relations.Link import Link

class Cascade(Displayment):
    for_object = 'App.DB.Search.Cascade'

    async def render_as_collection(self, orig_items, args, orig_collection = None):
        objects = list()

        def recurse(items, current_level: int = 0, max_depth: int = 30, objects_limit: int = 100):
            new_list = list()
            for object in items:
                if current_level > max_depth:
                    break

                item_dict = {
                    'item': None,
                    'link': None,
                    'links': list()
                }

                if object.isInstance(Link):
                    item_dict['link'] = object
                    item_dict['item'] = object.item
                else:
                    item_dict['item'] = object

                items = recurse(item_dict.get('item').getLinked(), current_level = current_level + 1, max_depth = max_depth, objects_limit = 10)
                item_dict['links'] = items[:objects_limit]

                new_list.append(item_dict)

            return new_list

        objects = recurse(orig_items)
        rel_url = '/?i=App.DB.Search'
        attrs = dict(self.request.rel_url.query)
        for key, val in attrs.items():
            if key in ['show_tmp', 'linked_to_type', 'linked_to', 'i', 'show_unlisted', 'act']:
                continue

            rel_url += '&' + key + '=' + val

        #print(objects)
        self.context.update({
            'items': objects,
            'args': args,
            'this_relative_url': rel_url,
            'ref': attrs.get('ref')
        })
        return self.render_string('Explorer/cascade.html')
