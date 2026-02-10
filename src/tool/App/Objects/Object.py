from .BaseModel import BaseModel
from .Section import Section
from .Hookable import Hookable

class Object(BaseModel, Section, Hookable):
    '''
    The base class of app, extended pydantic BaseModel.
    Fields can be flushed to json, also there is Section (log) functions and hooks.
    '''
    pass
