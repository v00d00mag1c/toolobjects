from .BaseModel import BaseModel
from .AllowExtraFields import AllowExtraFields
from .Section import Section
from .Hookable import Hookable
from .Configurable import Configurable
from .Linkable import Linkable
from .Convertable import Convertable
from .ModuleRequireable import ModuleRequireable
from .Submodules import Submodules
from .Saveable import Saveable
from typing import ClassVar, Any

class Object(BaseModel, AllowExtraFields, Linkable, Saveable, ModuleRequireable, Section, Submodules, Hookable, Configurable, Convertable):
    '''
    The base class of app, extended pydantic BaseModel.
    Fields can be flushed to json, also there is Section (log) functions and hooks.

    MRO's:
    Validable, Configurable, Submodules, Variableable
    '''

    self_name: ClassVar[str] = 'Object'
    call: Any = None # : Call
    _db: Any = None  # : ConnectionAdapterObject
