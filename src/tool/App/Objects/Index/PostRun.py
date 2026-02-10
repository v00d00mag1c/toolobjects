from App.Objects.Object import Object
from App import app

class PostRun(Object):
    @classmethod
    def mount(cls):
        for item in app.ObjectsList.getItems().toList():
            if item.is_inited == False:
                continue

            _module = item.getModule()

            for _item in _module.getAllSettings():
                if _item.role == 'config':
                    app.Config.values.compare.append(_item)
                elif _item.role == 'env':
                    app.Env.values.compare.append(_item)
                    print(app.Env.values.compare)
