from Files.Navigate import Navigate
from App.Objects.Client import Client
from App.Objects.Submodule import Submodule
from Files.Dir import Dir
from Files.File import File
from App import app

class FileManager(Client):
    @classmethod
    def getSubmodules(cls):
        return [
            Submodule(
                module = Dir,
            ),
            Submodule(
                module = File,
            ),
            Submodule(
                module = Navigate,
                role = ['wheel']
            )
        ]

    async def implementation(self, i):
        navigate = Navigate()

        return await navigate.execute({'path': str(app.app.cwd)})
