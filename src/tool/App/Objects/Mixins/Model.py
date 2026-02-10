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
        'exclude_defaults': False,
        'by_alias': False
    }

    # we can't use __init__ because of fields initialization, so we creating second constructor
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.__class__.init_hook(self)

    # *args and **kwargs are not passed
    def init_hook(self):
        pass

    @classmethod
    def isInstance(cls, object: PydanticBaseModel) -> bool:
        return cls._getClassNameJoined() == object._getClassNameJoined()

    @classmethod
    def isInMRO(cls, object: PydanticBaseModel) -> bool:
        for item in cls.getMRO():
            if item._getNameJoined() == object._getNameJoined():
                return True

    @classmethod
    def isSame(cls, object: PydanticBaseModel) -> bool:
        return cls._getNameJoined() == object._getNameJoined()

    @classmethod
    def getMRO(cls) -> list:
        return cls.__mro__

    @classmethod
    def canBeExecuted(cls):
        return hasattr(cls, 'execute')

    @classmethod
    def _getClassName(cls):
        '''
        Path to the current class + class name:

        a.b.c.d.d or something
        '''

        return cls._getName() + [cls._getModuleName()]

    @classmethod
    def _getModuleName(cls):
        return cls.__name__

    @classmethod
    def _getNameJoined(self):
        return ".".join(self._getName())

    @classmethod
    def _getClassNameJoined(cls, last_names_doubling: bool = False):
        '''
        _getClassName() but joined
        '''

        _name = cls._getClassName()
        if last_names_doubling == False:
            _name = _name[:-1]

        return ".".join(_name)

    @classmethod
    def _getName(self) -> list:
        _class = self.__mro__[0]
        _module = _class.__module__
        _parts = _module.split('.')
        #_parts = _parts[1:]

        return _parts

    @classmethod
    def _getClassNameJoined(cls) -> str:
        return cls.__module__

    @classmethod
    def _allowed_views(cls) -> list:
        '''
        Get View classes where. if None > allowed everywhere
        '''
        return None

    def to_minimal_json(self):
        return self.to_json(only_class_fields=True, by_alias=True, exclude_defaults = True)

    def to_extended_json(self):
        return self.to_json(
            exclude_internal = False,
            exclude = ['links', 'db_info', 'class_name'],
            convert_links = False,
            exclude_none = True,
            exclude_defaults = True,
            only_class_fields = False
        )

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

        excludes = ['internal_toolobjects_link_items']
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
        Model._dump_options['by_alias'] = by_alias

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
    def _getFieldsNames(cls, include_computed: bool = True) -> list[str]:
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

        try:
            for _item in [self.__class__.model_fields, self.__class__.model_computed_fields]:
                for field_name, val in _item.items():
                    _field_names.append(field_name)
                    _defaults[field_name] = getattr(val, 'default', None)

            if Model._dump_options['only_class_fields'] == True:
                _field_names = self.__class__.__annotations__

            for field_name in _field_names:
                field_name_key = field_name

                # Getting alias

                if field_name in self.__class__.model_fields:
                    _val_key = self.__class__.model_fields.get(field_name)

                    if getattr(_val_key, 'alias', None) != None and Model._dump_options.get('by_alias') == True:
                        field_name_key = _val_key.alias
                try:
                    if Model._dump_options['excludes'] != None and field_name in Model._dump_options['excludes']:
                        continue

                    if field_name in self.__class__._unserializable:
                        continue

                    value = getattr(self, field_name)
                    _field_name = None
                    _res = None

                    if isinstance(value, LinkInsertion):
                        value.setDb(self.getDb())
                        if Model._dump_options['convert_links'] == True:
                            _res = value.unwrap()
                        else:
                            _res = value
                    elif (isinstance(value, list) and value and isinstance(value[0], LinkInsertion)):
                        _res = []
                        for item in value:
                            item.setDb(self.getDb())

                            if Model._dump_options['convert_links'] == True:
                                _res.append(item.unwrap())
                    else:
                        _val = self._serializer(field_name, value)
                        if _val == None and self._dump_options.get('exclude_none') == True:
                            continue

                        if self._dump_options.get('exclude_defaults') == True:
                            if _val == _defaults.get(field_name, None):
                                continue

                        if hasattr(_val, 'setDb') and hasattr(self, 'setDb'):
                            _val.setDb(self.getDb())

                        _res = _val
                except Exception as e:
                    self.log_error(e, exception_prefix = 'Can\'t include field {0}'.format(field_name))

                result[field_name_key] = _res
            if Model._dump_options['include_extra'] == True and self.model_extra != None:
                for key, val in self.model_extra.items():
                    try:
                        result[key] = val
                    except Exception as e:
                        self.log_error(e, exception_prefix = 'Can\'t include field {0}'.format(key))
        except Exception as _e:
            self.log_error(e, exception_prefix='Error loading model {0}: '.format(self._getClassNameJoined()))

            if True:
                raise _e

        return result
