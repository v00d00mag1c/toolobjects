from App.Objects.Object import Object
from App import app

class PostRun(Object):
    @classmethod
    def mount(cls):
        for item in app.ObjectsList.getItems().toList():
            if item.is_inited == False:
                continue

            item.appendSettings()
