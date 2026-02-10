from App.Objects.Object import Object
from App.Objects.Relations.Submodule import Submodule

class Collection(Object):
    def init_hook(self):
        self.obj.collection = True

        return super().init_hook()

    @classmethod
    def _submodules(cls) -> list:
        from Data.Primitives.Collections.Manage import Manage

        return [
            Submodule(
                item = Manage,
                role = ['action']
            )
        ]
