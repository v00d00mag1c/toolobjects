from pydantic import BaseModel as PydanticBaseModel, computed_field, Field
from typing import ClassVar
from .classproperty import classproperty
from .Outer import Outer

class BaseModel(PydanticBaseModel):
    @computed_field
    @property
    def class_name(self) -> str:
        return self.getClassNameJoined()

    # we can't use __init__ because of fields initialization, so we creating second constructor
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.__class__.constructor(self)

    # *args and **kwargs are not passed
    def constructor(self):
        pass

    # model_dump alias
    def to_json(self, exclude_classname: bool = False):
        # todo remove
        exclude = []
        if exclude_classname == True:
            exclude.append('class_name')

        return self.model_dump(mode='json',exclude=exclude)

    @classmethod
    def getMRO(cls) -> list:
        return cls.__mro__

    @classmethod
    def canBeExecuted(cls):
        return True

    @classmethod
    def getClassName(cls):
        '''
        Path to the current class + class name:

        a.b.c.d.d or something
        '''
        return cls.getName() + [cls.__name__]

    @classmethod
    def getNameJoined(self):
        return ".".join(self.getName())

    @classmethod
    def getClassNameJoined(cls):
        '''
        getClassName() but joined
        '''

        return ".".join(cls.getClassName())

    @classmethod
    def getName(self) -> list:
        _class = self.__mro__[0]
        _module = _class.__module__
        _parts = _module.split('.')
        #_parts = _parts[1:]

        return _parts

    @classmethod
    def getClassModule(cls) -> str:
        return cls.__module__

    '''
    @classmethod
    def canBeUsedAt(cls, at: str):
        return at in cls.getAvailableContexts()
    '''

    @classmethod
    def mount(cls):
        '''
        Method that called after loading
        '''
        pass

    def __init_subclass__(cls):
        for item in cls.__mro__:
            if hasattr(item, "init_subclass") == True:
                getattr(item, "init_subclass")(cls)

            if isinstance(item, PydanticBaseModel):
                item.__init_subclass__()
