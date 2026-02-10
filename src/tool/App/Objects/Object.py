from .Mixins.BaseModel import BaseModel
from .Mixins.Section import Section
from .Mixins.Hookable import Hookable
from .Mixins.Configurable import Configurable
from .Mixins.Linkable import Linkable
from .Mixins.Convertable import Convertable
from .Mixins.ModuleRequireable import ModuleRequireable
from .Mixins.Submodulable import Submodulable
from App.ACL.Limitable import Limitable
from App.DB.DBInsertable import DBInsertable
from typing import ClassVar
from pydantic import ConfigDict
from App import app

class Object(BaseModel, 
             Linkable, 
             ModuleRequireable, 
             Section, 
             Submodulable, 
             Hookable, 
             Configurable, 
             Convertable, 
             DBInsertable,
             Limitable):

    self_name: ClassVar[str] = 'Object'
    model_config = ConfigDict(extra='allow')

    @classmethod
    def _documentation(cls):
        return None

    async def update(self, old: BaseModel, response: BaseModel) -> BaseModel:
        return response

    @classmethod
    def asArgument(cls, val: str) -> BaseModel:
        if isinstance(val, str):
            _val = app.ObjectsList.getByName(key = val)
            if _val == None:
                return None

            return _val.getModule()

        # isinstance not works
        if hasattr(val, 'self_name'):
            return val

        return super().asArgument(val)

