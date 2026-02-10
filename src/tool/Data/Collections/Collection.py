from App.Objects.Client import Client

class Collection(Client):
    def init_hook(self):
        self.obj.collection = True

        return super().init_hook()
