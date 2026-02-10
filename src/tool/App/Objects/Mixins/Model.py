from pydantic import BaseModel as PydanticBaseModel
from typing import Literal, ClassVar, Any
from datetime import datetime
from pydantic import model_serializer
from App.Objects.Relations.LinkInsertion import LinkInsertion

class Model(PydanticBaseModel):
    _unserializable: ClassVar[list[str]] = ['_dump_options', '_unserializable']

    # model_dump does not checks this params, so doing workaround. TODO remove
    _dump_options: ClassVar[dict] = {
        'convert_links': False,
        'include_extra': True,
        'excludes': None,
        'internal_fields': ['meta', 'saved_via', 'links', 'db_info'],
        'only_class_fields': False,
        'exclude_none': False,
        'exclude_defaults': False
    }

    # we can't use __init__ because of fields initialization, so we creating second constructor
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.__class__.init_hook(self)

    # *args and **kwargs are not passed
    def init_hook(self):
        pass

    def isInstance(self, object: PydanticBaseModel) -> bool:
        return self.getClassNameJoined() == object.getClassNameJoined()

    @classmethod
    def isSame(cls, object: PydanticBaseModel) -> bool:
        return cls.getNameJoined() == object.getNameJoined()

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

        return cls.getName() + [cls.getModuleName()]

    @classmethod
    def getModuleName(cls):
        return cls.__name__

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
        Get View classes where. if None > allowed everywhere
        '''
        return None

    def minimal_json(self):
        return self.to_json(only_class_fields=True, by_alias=True)

    def to_json(self, 
                convert_links: Literal['unwrap', 'none'] = 'unwrap', 
                exclude_internal: bool = False,
                exclude_none: bool = False,
                exclude: list[str] = [],
                exclude_defaults: bool = False,
                by_alias: bool = True,
                include_extra: bool = True,
                only_class_fields: bool = False):
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

        Model._dump_options['include_extra'] = include_extra
        Model._dump_options['excludes'] = excludes
        Model._dump_options['convert_links'] = convert_links == 'unwrap'
        Model._dump_options['only_class_fields'] = only_class_fields
        Model._dump_options['exclude_none'] = exclude_none
        Model._dump_options['exclude_defaults'] = exclude_defaults

        results = self.model_dump(mode = 'json', 
                exclude_none = exclude_none,
                exclude_defaults = exclude_defaults,
                by_alias = by_alias)

        return results

    def __init_subclass__(cls):
        for item in cls.__mro__:
            if hasattr(item, "init_subclass") == True:
                getattr(item, "init_subclass")(cls)

            if isinstance(item, PydanticBaseModel):
                item.__init_subclass__()

    def _serializer(self, field_name: str, value: Any):
        if isinstance(value, datetime):
            return value.timestamp()

        if True:
            for key, val in self.__pydantic_decorators__.field_serializers.items():
                if field_name in val.info.fields:
                    return val.func(self, value)

        return value

    @classmethod
    def getFieldsNames(cls, include_computed: bool = True) -> list[str]:
        names = list()
        for name in cls.model_fields:
            names.append(name)
        if include_computed == True:
            for name in cls.model_computed_fields:
                names.append(name)

        return names

    @model_serializer
    def serialize_model_with_links(self) -> dict:
        '''
        Function for json convertation. It exists because we need to convert LinkInsertions
        '''

        # ???
        result = dict()
        _field_names = list()
        _defaults = dict()

        for _item in [self.__class__.model_fields, self.__class__.model_computed_fields]:
            for field_name, val in _item.items():
                _field_names.append(field_name)
                _defaults[field_name] = getattr(val, 'default', None)

        if Model._dump_options['only_class_fields'] == True:
            _field_names = self.__class__.__annotations__

        for field_name in _field_names:
            if Model._dump_options['excludes'] != None and field_name in Model._dump_options['excludes']:
                continue

            if field_name in self.__class__._unserializable:
                continue

            value = getattr(self, field_name)

            if isinstance(value, LinkInsertion):
                value.setDb(self.getDb())
                if Model._dump_options['convert_links'] == True:
                    result[field_name] = value.unwrap()
                else:
                    result[field_name] = value
            elif (isinstance(value, list) and value and isinstance(value[0], LinkInsertion)):
                result[field_name] = []
                for item in value:
                    item.setDb(self.getDb())

                    if Model._dump_options['convert_links'] == True:
                        result.get('field_name').append(item.unwrap())
            else:
                _val = self._serializer(field_name, value)
                if _val == None and self._dump_options.get('exclude_none') == True:
                    continue

                if self._dump_options.get('exclude_defaults') == True:
                    if _val == _defaults.get(field_name, None):
                        continue

                if hasattr(_val, 'setDb') and hasattr(self, 'setDb'):
                    _val.setDb(self.getDb())

                result[field_name] = _val

        if Model._dump_options['include_extra'] == True and self.model_extra != None:
            for key, val in self.model_extra.items():
                result[key] = val

        return result
