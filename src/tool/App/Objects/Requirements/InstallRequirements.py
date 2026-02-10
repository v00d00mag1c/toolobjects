from App.Objects.Act import Act
from App.Objects.Arguments.ArgumentDict import ArgumentDict
from App.Objects.Arguments.Assertions.NotNoneAssertion import NotNoneAssertion
from App.Objects.Arguments.Argument import Argument
from App.Objects.Executable import Executable
from App.Responses.AnyResponse import AnyResponse

class InstallRequirements(Act):
    @classmethod
    def getArguments(cls):
        return ArgumentDict(items=[
            Argument(
                name = 'object',
                orig = Executable,
                assertions = [NotNoneAssertion()]
            )
        ])

    async def implementation(self, i):
        import subprocess, sys

        _object = i.get('object')
        modules = _object.getNotInstalledModules()
        if len(modules) < 1:
            self.log(f"plugin {_object.getNameJoined()} does not contains uninstalled modules")

        else:
            _pars = [sys.executable, '-m', 'pip', 'install']
            for _module in modules:
                _pars.append(_module.getName())

            subprocess.call(_pars)

        return AnyResponse(data = modules)
