from .Mixins.BaseModel import BaseModel
from .Mixins.Section import Section
from .Mixins.Hookable import Hookable
from .Mixins.Configurable import Configurable
from .Mixins.Linkable import Linkable
from .Mixins.Convertable import Convertable
from .Mixins.ModuleRequireable import ModuleRequireable
from .Mixins.Submodulable import Submodulable
from .Mixins.Saveable import Saveable
from .Mixins.Updateable import Updateable
from App.ACL.Limitable import Limitable
from App.Storage.DB.DBInsertable import DBInsertable
from typing import ClassVar
from pydantic import ConfigDict
from App import app

class Object(BaseModel, 
             Linkable, 
             Saveable, 
             ModuleRequireable, 
             Section, 
             Submodulable, 
             Hookable, 
             Configurable, 
             Convertable, 
             DBInsertable,
             Limitable,
             Updateable):
    self_name: ClassVar[str] = 'Object'

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

    @classmethod
    def _documentation(cls):
        return None

    model_config = ConfigDict(extra='allow')
