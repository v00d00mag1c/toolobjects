from App.Objects.Object import Object
from App.Objects.Queue.LinkValue import LinkValue
from pydantic import Field
from App import app

class OutputItem(Object):
    response_name: str = Field(default = 'App.Objects.Responses.ObjectsList')
    value: str = None

    def apply(self, prestart: list, items: list):
        obj = app.ObjectsList.getByName(self.response_name)
        vals = LinkValue(value = self.value)

        return obj.getModule().fromItems(vals.toString(prestart, items))
