from App.Client.Displayment import Displayment

class StorageUUID(Displayment):
    for_object = 'App.Storage.StorageUUID'

    async def render_as_object(self, item):
        self.context.update({
            'items': [item],
        })

        return self.render_string('Storage/storage_uuid.html')
