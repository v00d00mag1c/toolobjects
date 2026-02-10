from App.Objects.Act import Act
from App.Objects.Arguments.ArgumentDict import ArgumentDict
from App.Objects.Arguments.Assertions.NotNone import NotNone
from App.Objects.Arguments.ListArgument import ListArgument
from App.Objects.Requirements.Requirement import Requirement

class Install(Act):
    @classmethod
    def _arguments(cls):
        return ArgumentDict(items=[
            ListArgument(
                name = 'requirements',
                orig = Requirement,
                assertions = [NotNone()]
            )
        ])

    def _implementation(self, i):
        import subprocess, sys

        requirements = i.get('requirements')

        _pars = [sys.executable, '-m', 'pip', 'install']
        for _module in requirements:
            _pars.append(_module.get_name())

        subprocess.call(_pars)
