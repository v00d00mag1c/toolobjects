from pydantic import BaseModel as PydanticBaseModel, computed_field, model_serializer, field_validator
from App.Objects.Misc.LinkInsertion import LinkInsertion
from typing import Literal, ClassVar, Any
from datetime import datetime

class BaseModel(PydanticBaseModel):
    '''
    Pydantic BaseModel with some functions
    '''

    # Workaround to add model_serializer (that is in Linkable) check
    _convert_links: ClassVar[bool] = False
    _include_extra: ClassVar[bool] = True
    _excludes: ClassVar[list[str]] = None
    _internal_fields: ClassVar[list[str]] = ['meta', 'saved_via', 'links', 'db_info']
    _unserializable: ClassVar[list[str]] = ['_only_class_fields', '_convert_links', '_include_extra', '_excludes', '_internal_fields', '_unserializable']
    _only_class_fields: bool = False

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
                by_alias: bool = True,
                include_extra: bool = True,
                only_class_fields: bool = True):
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

        BaseModel._convert_links = False
        BaseModel._include_extra = include_extra
        BaseModel._excludes = excludes
        BaseModel._convert_links = convert_links == 'unwrap'
        BaseModel._only_class_fields = only_class_fields

        results = self.model_dump(mode = 'json', 
                exclude_none = exclude_none,
                by_alias = by_alias)

        return results

    @classmethod
    def asArgument(cls, val: Any):
        if isinstance(val, cls):
            return val

        return cls.model_validate(val)

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
    def getClassNameJoined(cls, last_names_doubling: bool = False):
        '''
        getClassName() but joined
        '''

        _name = cls.getClassName()
        if last_names_doubling == False:
            _name = _name[:-1]

        return ".".join(_name)

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

    @classmethod
    def getAllowedViews(cls) -> list:
        '''
        Get View classes where. If None -> allowed everywhere
        '''
        return None

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

    def _serializer(self, value: Any):
        if isinstance(value, datetime):
            return value.timestamp()

        return value

    @model_serializer
    def serialize_model_with_links(self) -> dict:
        result = dict()
        _field_names = list()
        for field_name in self.__class__.model_fields:
            _field_names.append(field_name)
        for field_name in self.__class__.model_computed_fields:
            _field_names.append(field_name)

        if self.__class__._only_class_fields == True:
            _field_names = self.__class__.__annotations__

        for field_name in _field_names:
            if BaseModel._excludes != None and field_name in BaseModel._excludes:
                continue

            if field_name in self.__class__._unserializable:
                continue

            value = getattr(self, field_name)

            if isinstance(value, LinkInsertion):
                value.setDb(self.getDb())
                if BaseModel._convert_links == True:
                    result[field_name] = value.unwrap()
                else:
                    result[field_name] = value
            elif (isinstance(value, list) and value and isinstance(value[0], LinkInsertion)):
                result[field_name] = []
                for item in value:
                    item.setDb(self.getDb())

                    if BaseModel._convert_links == True:
                        result.get('field_name').append(item.unwrap())
            else:
                result[field_name] = self._serializer(value)

        if BaseModel._include_extra == True:
            for key, val in self.model_extra.items():
                result[key] = val

        return result
