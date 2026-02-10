from .BaseModel import BaseModel
from .Section import Section
from .Hookable import Hookable

class Object(BaseModel, Section, Hookable):
    pass
