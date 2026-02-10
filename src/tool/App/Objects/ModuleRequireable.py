from importlib.metadata import distributions
from pydantic import BaseModel

class ModuleRequireable(BaseModel):
    @classmethod
    def getRequiredModules(self):
        '''
        pip modules that required by object
        '''
        return []

    @classmethod
    def getNotInstalledModules(self) -> list:
        all_installed = {dist.metadata["Name"].lower() for dist in distributions()}
        satisf_libs = []
        not_libs = []

        for required_module in self.getRequiredModules():
            module_versions = required_module.split("==")
            module_name = module_versions[0]

            if module_name in all_installed:
                satisf_libs.append(module_name)
            else:
                not_libs.append(module_name)

        return not_libs

    @classmethod
    def isRequiredModulesInstalled(cls) -> bool:
        return len(cls.getNotInstalledModules()) == 0
