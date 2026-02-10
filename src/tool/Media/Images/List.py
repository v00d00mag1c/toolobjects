from App.Objects.Client import Client
from App.Objects.Relations.Submodule import Submodule
from Media.Images.Image import Image
from Media.Images.AddImages import AddImages

class List(Client):
    @classmethod
    def _submodules(cls) -> list:
        return [
            Submodule(
                item = Image,
                role = ['object']
            ),
            Submodule(
                item = AddImages,
                role = ['action']
            )
        ]

    async def implementation(self, i):
        pass
