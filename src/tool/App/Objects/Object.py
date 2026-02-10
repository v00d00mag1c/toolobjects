from .BaseModel import BaseModel
from .Section import Section
from .Hookable import Hookable
from .Configurable import Configurable
from .Convertable import Convertable
from .ModuleRequireable import ModuleRequireable
from .Submodules import Submodules
from typing import ClassVar, Any

class Object(BaseModel, ModuleRequireable, Section, Submodules, Hookable, Configurable, Convertable):
    '''
    The base class of app, extended pydantic BaseModel.
    Fields can be flushed to json, also there is Section (log) functions and hooks.

    MRO's:
    Validable, Configurable, Submodules, Variableable
    '''

    self_name: ClassVar[str] = 'Object'
    call: Any = None # : Call
    _db: Any = None  # : ConnectionAdapterObject

