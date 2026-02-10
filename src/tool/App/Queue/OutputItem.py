from App.Objects.Object import Object
from App.Queue.LinkValue import LinkValue
from App import app

class OutputItem(Object):
    key: str = None
    response: str = None

    def apply(self, prestart: list, items: list):
        obj = app.app.objects.getByName(self.response)

        '''
        It passes key as *args, so add repr=True to common field
        '''
        vals = LinkValue(value = self.key)

        return obj.getModule().fromItems(vals.toString(prestart, items))
