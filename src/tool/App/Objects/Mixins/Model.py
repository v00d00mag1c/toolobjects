from pydantic import BaseModel as PydanticBaseModel
from typing import Literal, ClassVar, Any
from datetime import datetime
from App.Objects.Mixins.Section import Section
from pydantic import model_serializer
from App.Objects.Relations.LinkInsertion import LinkInsertion

class Model(PydanticBaseModel, Section):
    # Unserializable fields:

    # Like "exclude" on Field: won't be serialized anywhere
    _unserializable: ClassVar[list[str]] = ['_dump_options', '_unserializable']

    # Fields with names from this list won't be serialized on output, but will on db insertion
    _unserializable_on_output: ClassVar[list[str]] = []

    # model_dump does not checks this params, so doing workaround. TODO remove
    _dump_options: ClassVar[dict] = {
        'convert_links': False,
        'include_extra': True,
        'excludes': None,
        'internal_fields': ['meta', 'saved_via', 'links', 'db_info'],
        'only_class_fields': False,
        'exclude_none': False,
        'exclude_defaults': False,
        'by_alias': False,
        'exclude_that_excluded': True,
        'include_computed_fields': False,
        'links_replace': {},
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
            if hasattr(item, '_getNameJoined'):
                if item._getNameJoined() == object._getNameJoined():
                    return True

        return False

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
    def _getNameJoined(self):
        return ".".join(self._getName())

    @classmethod
    def _getClassNameJoined(cls) -> str:
        return cls.__module__

    @classmethod
    def hasAttr(cls, name):
        return hasattr(cls, name)

    @classmethod
    def is_same_name(cls, name: str) -> bool:
        return cls._getNameJoined() == name

    @classmethod
    def is_name_equals(cls, name: str) -> bool:
        return cls._getNameJoined() == name or cls._getClassNameJoined() == name

    @classmethod
    def mro_name_check(cls, names: list) -> bool:
        for item in cls.getMRO():
            for name in names:
                if hasattr(item, 'is_name_equals') and item.is_name_equals(name):
                    return True

        return False

    @classmethod
    def _allowed_views(cls) -> list:
        '''
        Views where object can be executed. If zero > will be available everywhere
        '''

        return cls.getSubmodules(with_role = ['allowed_view'])

    def to_minimal_json(self):
        return self.to_json(only_class_fields = True, by_alias = True, exclude_defaults = True)

    def to_db_json(self):
        return self.to_json(
            exclude_internal = False,
            exclude = ['links', 'db_info', 'class_name', 'any_name', 'any_description'],
            exclude_output_values = False,
            convert_links = 'none',
            exclude_none = True,
            exclude_defaults = True,
            only_class_fields = False,
            include_computed_fields = False
        )

    def to_json(self, 
                convert_links: Literal['unwrap', 'none'] = 'unwrap', 
                exclude_internal: bool = False,
                exclude_none: bool = False,
                exclude_output_values: bool = True,
                exclude: list[str] = [],
                exclude_defaults: bool = False,
                by_alias: bool = True,
                include_extra: bool = True,
                only_class_fields: bool = False,
                include_computed_fields: bool = True):
        '''
        convert_links: replace LinkInsertions with their "unwrap()" function results

        exclude_internal: exclude fields from "self._internal_fields"

        exclude_none: exclude None values

        exclude: list with excluded fields

        include_extra: include "model_computed_fields"
        '''

        excludes = ['links']

        '''
        if exclude_internal == True:
            for _exclude in self._internal_fields:
                excludes.append(_exclude)
        '''

        if exclude_output_values:
            for _exclude in self._unserializable_on_output:
                excludes.append(_exclude)

        for item in exclude:
            excludes.append(item)

        # I don't know a better way to pass values to serializer
        Model._dump_options['include_extra'] = include_extra
        Model._dump_options['excludes'] = excludes
        Model._dump_options['convert_links'] = convert_links == 'unwrap'
        Model._dump_options['only_class_fields'] = only_class_fields
        Model._dump_options['exclude_none'] = exclude_none
        Model._dump_options['exclude_defaults'] = exclude_defaults
        Model._dump_options['by_alias'] = by_alias
        Model._dump_options['include_computed_fields'] = include_computed_fields

        results = self.model_dump(mode = 'json', 
                exclude_none = exclude_none,
                exclude_defaults = exclude_defaults,
                by_alias = by_alias,
                exclude_computed_fields = include_computed_fields == False)

        return results

    @classmethod
    def model_validate_override(cls, data: dict | Any):
        return cls.model_validate(data)

    @classmethod
    async def from_some_api(cls, data: dict | Any):
        return cls.model_validate_override(data)

    @classmethod
    async def from_xml(cls, data: dict):
        return await cls.from_some_api(data)

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

        result = dict()
        _field_names = list()
        _defaults = dict()

        try:
            _fields_to_search = [self.__class__.model_fields]
            if Model._dump_options['include_computed_fields'] == True:
                _fields_to_search.append(self.__class__.model_computed_fields)

            for _item in _fields_to_search:
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
                    _exclude = getattr(_val_key, 'exclude', None)

                    if getattr(_val_key, 'alias', None) != None and Model._dump_options.get('by_alias') == True:
                        field_name_key = _val_key.alias

                    if Model._dump_options.get('exclude_that_excluded'):
                        if _exclude == True:
                            continue

                try:
                    if Model._dump_options['excludes'] != None and field_name in Model._dump_options['excludes']:
                        continue

                    if field_name in self.__class__._unserializable:
                        continue

                    value = getattr(self, field_name)
                    _res = None

                    if isinstance(value, LinkInsertion):
                        value.setDb(self.getDb())

                        if value != None and value.link != None and type(value.link) == int:
                            _repl = self._dump_options['links_replace'].get(value.link)
                            if _repl != None:
                                value.link = _repl

                        if Model._dump_options['convert_links'] == True:
                            _res = value.unwrap()
                        else:
                            # self.log('not converting links')

                            assert value.link != None and value.field != None, 'broken link insertion'

                            if type(value.link) != int:
                                assert value.link.hasDb() == True, 'broken link insertion: it did not flushed'

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
                except AssertionError as e:
                    raise e
                except Exception as e:
                    self.log_error(e, exception_prefix = 'Can\'t include field {0}: '.format(field_name))
                    _res = None
                    # Or do "continue"? dk

                result[field_name_key] = _res
            if Model._dump_options['include_extra'] == True and self.model_extra != None:
                for key, val in self.model_extra.items():
                    try:
                        result[key] = val
                    except Exception as e:
                        self.log_error(e, exception_prefix = 'Can\'t include field {0}: '.format(key))
        except AssertionError as e:
            raise e
        except Exception as _e:
            self.log_error(e, exception_prefix='Error loading model {0}: '.format(self._getClassNameJoined()))

            if True:
                raise _e

        return result

    def _get(self, field, default = None):
        # If field is link insertion, unwrapping it and getting as normal value
        # also it append current _db to the property if it possible

        _field = getattr(self, field, default)

        if hasattr(_field, 'setDb'):
            _field.setDb(self.getDb())

        if hasattr(_field, '_link_insertion_type') == True:
            return _field.unwrap()

        return _field

    def _set(self, field, value = None):
        setattr(self, field, value)
