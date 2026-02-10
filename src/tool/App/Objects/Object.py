from .BaseModel import BaseModel
from .Section import Section
from .Hookable import Hookable
from .Configurable import Configurable
from .Linkable import Linkable
from .Convertable import Convertable
from .ModuleRequireable import ModuleRequireable
from .Submodulable import Submodulable
from .Saveable import Saveable
from App.ACL.Limitable import Limitable
from App.Storage.DB.DBInsertable import DBInsertable
from App.Daemons.Daemonable import Daemonable
from typing import ClassVar
from pydantic import ConfigDict

class Object(BaseModel, Linkable, Saveable, ModuleRequireable, Section, Submodulable, Hookable, Configurable, Convertable, DBInsertable, Daemonable, Limitable):
    '''
    The base class of app
    '''

    model_config = ConfigDict(extra='allow')
    self_name: ClassVar[str] = 'Object'
