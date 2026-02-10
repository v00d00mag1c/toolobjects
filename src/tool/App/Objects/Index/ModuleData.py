from App.Objects.Mixins.BaseModel import BaseModel
from pydantic import Field

class ModuleData(BaseModel):
    name: str = Field(default = None)
    arguments: list = Field(default = [])
    submodules: list = Field(default = [])
    requirements: list = Field(default = [])
    settings: list = Field(default = [])
    instance_values: dict = Field(default = None)

    @staticmethod
    def from_module(module, include_subs: bool = False, 
                    include_args: bool = False, 
                    include_settings: bool = False,
                    include_requirements: bool = False,
                    include_variables: bool = False):
        _dt = ModuleData()
        _dt.name = module._getNameJoined()

        # TODO rewrite
        if include_subs:
            for submodule in module.getSubmodules():
                _dt.submodules.append(submodule)

        if include_args:
            if hasattr(module, 'getArguments'):
                for val in module.getArguments().toList():
                    _dt.arguments.append(val)

        if include_requirements:
            for req in module.getRequirements():
                _dt.requirements.append(req)

        if include_settings:
            for option in module.getSettings():
                _dt.settings.append(option)

        return _dt
