from App.Objects.Object import Object

class Collection(Object):
    def init_hook(self):
        self.obj.collection = True

        return super().init_hook()
