from importlib.metadata import distributions
from pydantic import BaseModel

class ModuleRequireable(BaseModel):
    @classmethod
    def _requirements(cls):
        '''
        pip modules that required by object
        '''
        return []

    @classmethod
    def getRequirements(cls):
        return cls._requirements()

    @classmethod
    def getNotInstalledModules(self) -> list:
        all_installed = {dist.metadata["Name"].lower() for dist in distributions()}
        satisf_libs = []
        not_libs = []

        for required_module in self._requirements():
            if required_module.name in all_installed:
                satisf_libs.append(required_module)
            else:
                not_libs.append(required_module)

        return not_libs

    @classmethod
    def isRequiredModulesInstalled(cls) -> bool:
        return len(cls.getNotInstalledModules()) == 0

    @classmethod
    def check_requirements(cls):
        assert cls.isRequiredModulesInstalled()
