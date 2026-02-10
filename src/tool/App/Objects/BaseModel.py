from pydantic import BaseModel as PydanticBaseModel, computed_field, Field
from App.Objects.LinkInsertion import LinkInsertion

class BaseModel(PydanticBaseModel):
    '''
    Pydantic BaseModel with some functions
    '''

    # Workaround to add model_serializer (that is in Linkable) check
    _convert_links: bool = False

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

    def to_json(self, convert_links: bool = True, exclude_internal: bool = True):
        '''
        convert_links: replace LinkInsertions with their "unwrap()" function results

        exclude_internal: exclude fields from "self._internal_fields"
        '''
        excludes = set()

        if exclude_internal == True:
            excludes = self._internal_fields

        self._convert_links = convert_links

        return self.model_dump(mode='json', exclude=excludes)

    @classmethod
    def getMRO(cls) -> list:
        return cls.__mro__

    @classmethod
    def canBeExecuted(cls):
        return hasattr(cls, 'execute')

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
