from .BaseModel import BaseModel
from .AllowExtraFields import AllowExtraFields
from .Section import Section
from .Hookable import Hookable
from .Configurable import Configurable
from .Linkable import Linkable
from .Convertable import Convertable
from .ModuleRequireable import ModuleRequireable
from .Submodulable import Submodulable
from .Saveable import Saveable
from App.Storage.DB.DBInsertable import DBInsertable
from App.Daemons.Daemonable import Daemonable
from typing import ClassVar

class Object(BaseModel, AllowExtraFields, Linkable, Saveable, ModuleRequireable, Section, Submodulable, Hookable, Configurable, Convertable, DBInsertable, Daemonable):
    '''
    The base class of app, extended pydantic BaseModel.
    Fields can be flushed to json, also there is Section (log) functions and hooks.

    MRO's:
    Validable, Configurable, Submodulable, Variableable
    '''

    self_name: ClassVar[str] = 'Object'
