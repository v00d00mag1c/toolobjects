from App.Objects.Act import Act
from App.Objects.Requirements.Install import Install
from App import app

class InstallEvery(Act):
    async def _implementation(self, i):
        import subprocess, sys

        self.log('This act will load every object.')
        _modules = list()

        for item in app.ObjectsList.getItems().toList():
            try:
                _module = item.getModule()
                _reqs = _module.getRequirements()
                _len = len(_reqs)

                if _len > 0:
                    self.log("module {0} has {1} requirements".format(_module.getClassNameJoined(), _len))

                    for req in _reqs:
                        _modules.append(req)
            except Exception as e:
                self.log_error(e, not_log = True)

        await Install().execute({
            'requirements': _modules
        })
