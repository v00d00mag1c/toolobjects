from App.Objects.Act import Act
from App.Objects.Arguments.ArgumentDict import ArgumentDict
from App.Objects.Arguments.Assertions.NotNone import NotNone
from App.Objects.Arguments.Argument import Argument
from App.Objects.Executable import Executable
from App.Objects.Requirements.Install import Install

class InstallFromObject(Act):
    @classmethod
    def _arguments(cls):
        return ArgumentDict(items=[
            Argument(
                name = 'object',
                orig = Executable,
                assertions = [NotNone()]
            )
        ])

    async def _implementation(self, i):
        _object = i.get('object')
        _requirements = _object.getNotInstalledModules()
        if len(_requirements) < 1:
            self.log(f"plugin {_object.getNameJoined()} does not contains uninstalled modules")
        else:
            await Install().execute({
                'requirements': _requirements
            })
