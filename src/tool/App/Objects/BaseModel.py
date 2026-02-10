from pydantic import BaseModel as PydanticBaseModel, computed_field, model_serializer
from App.Objects.LinkInsertion import LinkInsertion
from typing import Literal, ClassVar

class BaseModel(PydanticBaseModel):
    '''
    Pydantic BaseModel with some functions
    '''

    # Workaround to add model_serializer (that is in Linkable) check
    _convert_links: ClassVar[bool] = False
    _include_extra: ClassVar[bool] = True
    _excludes: ClassVar[list[str]] = None

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

    def to_json(self, 
                convert_links: Literal['unwrap', 'none'] = 'none', 
                exclude_internal: bool = False,
                exclude_none: bool = False,
                exclude: list[str] = [],
                include_extra: bool = True):
        '''
        convert_links: replace LinkInsertions with their "unwrap()" function results

        exclude_internal: exclude fields from "self._internal_fields"

        exclude_none: exclude None values

        exclude: list with excluded fields

        include_extra: include "model_computed_fields"
        '''

        excludes = []
        if exclude_internal == True:
            for _exclude in self._internal_fields:
                excludes.append(_exclude)

        for item in exclude:
            excludes.append(item)

        PydanticBaseModel._convert_links = False
        PydanticBaseModel._include_extra = include_extra
        PydanticBaseModel._excludes = excludes
        PydanticBaseModel._convert_links = convert_links == 'unwrap'

        results = self.model_dump(mode = 'json', 
                exclude_none = exclude_none)

        return results

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

    @model_serializer
    def serialize_model_with_links(self) -> dict:
        result = dict()
        _field_names = list()
        for field_name in self.__class__.model_fields:
            _field_names.append(field_name)
        for field_name in self.__class__.model_computed_fields:
            _field_names.append(field_name)

        for field_name in _field_names:
            if PydanticBaseModel._excludes != None and field_name in PydanticBaseModel._excludes:
                continue

            value = getattr(self, field_name)

            if isinstance(value, LinkInsertion):
                value.setDb(self.getDb())
                if PydanticBaseModel._convert_links == True:
                    result[field_name] = value.unwrap()
                else:
                    result[field_name] = value
            elif (isinstance(value, list) and value and isinstance(value[0], LinkInsertion)):
                result[field_name] = []
                for item in value:
                    item.setDb(self.getDb())

                    if PydanticBaseModel._convert_links == True:
                        result.get('field_name').append(item.unwrap())
            else:
                result[field_name] = value

        if PydanticBaseModel._include_extra == True:
            for key, val in self.model_extra.items():
                result[key] = val

        return result
