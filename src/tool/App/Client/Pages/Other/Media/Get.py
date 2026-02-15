from App.Client.Displayment import Displayment
from App.Storage.Item.StorageItem import StorageItem
from Media.Media import Media
from App import app

class Get(Displayment):
    for_object = 'Media.Get'

    async def render_as_page(self, args = {}):
        query = self.request.rel_url.query
        act = query.get('act')
        media_types = list()
        orig_item = self.get_link_item()

        assert orig_item != None

        storage_name = ''
        if orig_item.isInstance(StorageItem):
            storage_name = orig_item.name
        else:
            storage_name = orig_item.getDbName()

        for item in app.ObjectsList.getObjectsByCategory(['Media']):
            _module = item.getModule()
            if _module.isInMRO(Media) and _module._getNameJoined() != 'Media.Media':
                media_types.append(_module)

        #for item in items.getItems():
            #item.local_obj.make_public()

        self.context.update({
            'media_types': media_types,
            'orig_item': orig_item,
            'storage_name': storage_name,
            'ref': query.get('ref'),
            'act': act
        })

        if self.is_post():
            data = await self.request.post()
            object_name = data.get('object')
            args = {
                'object': object_name,
                'symlink': data.get('media_symlink') == 'on'
            }

            match (act):
                case 'url':
                    args.update({
                        'url': data.get('media_url'),
                        'referer': data.get('media_referer')
                    })
                case 'dir':
                    args.update({
                        'dir': data.get('media_dir')
                    })
                case 'path':
                    args.update({
                        'path': data.get('media_path')
                    })
                case 'file':
                    args.update({
                        'storage_unit': data.get('media_storage_unit').split(',')
                    })

            new_items = await self._execute('Media.Get', args)

            return self.redirect(self._flush_creation(orig_item, new_items.items))

        return self.render_template('Other/Media/get.html')
