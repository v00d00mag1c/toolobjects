from App.Objects.Client import Client
from App.Objects.Relations.Submodule import Submodule
from Files.FileTypes.Image import Image
from Data.Gallery.AddImages import AddImages

class Gallery(Client):
    @classmethod
    def getSubmodules(cls) -> list:
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
