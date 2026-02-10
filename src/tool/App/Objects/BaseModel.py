from importlib.metadata import distributions
from pydantic import BaseModel as PydanticBaseModel, computed_field
from .classproperty import classproperty
from .Outer import Outer

class BaseModel(PydanticBaseModel):
    # we can't use __init__ because of fields initialization, so we creating second constructor
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.__class__.constructor(self)

    # *args and **kwargs are not passed
    def constructor(self):
        pass

    # model_dump alias
    def to_json(self):
        return self.model_dump(mode='json')

    def init_subclass(cls):
        cls.meta = cls.Meta(cls)
        # cls.submodules = cls.Submodules(cls)

    def __init_subclass__(cls):
        for item in cls.__mro__:
            if hasattr(item, "init_subclass") == True:
                getattr(item, "init_subclass")(cls)

            if isinstance(item, PydanticBaseModel):
                item.__init_subclass__()

    class Meta(Outer):
        @property
        def mro(self) -> list:
            return self.outer.__mro__

        @property
        def available_at(self):
            return ['web', 'cli', '*']

        @property
        def required_modules(self):
            return []

        @property
        def is_abstract(self):
            return False

        @property
        def is_hidden(self) -> bool:
            return getattr(self, "hidden", False) == True

        @property
        def can_be_executed(self):
            return self.is_abstract() == False and self.is_hidden() == False # and self.outer hasclass Execute

        @property
        def get_not_installed_required_modules(cls) -> list:
            all_installed = {dist.metadata["Name"].lower() for dist in distributions()}
            satisf_libs = []
            not_libs = []

            for required_module in cls.required_modules:
                module_versions = required_module.split("==")
                module_name = module_versions[0]

                if module_name in all_installed:
                    satisf_libs.append(module_name)
                else:
                    not_libs.append(module_name)

            return not_libs

        @property
        def is_required_modules_installed(cls) -> bool:
            return len(cls.get_not_installed_required_modules()) > 0

        @property
        def main_module(cls):
            if hasattr(cls, "outer") == False:
                return None

            for item in cls.outer.__mro__:
                if getattr(item, "outer", None) != None:
                    return item.outer

        @property
        def name_joined(self):
            return ".".join(self.name)

        @property
        def class_name(self):
            return self.name + [self.outer.__name__]

        @property
        def class_name_str(self):
            return ".".join(self.class_name)

        @property
        def name(self) -> list:
            _class = self.outer.__mro__[0]
            _module = _class.__module__
            _parts = _module.split('.')
            #_parts = _parts[1:]

            return _parts

        @property
        def class_module(cls) -> str:
            return cls.outer.__module__

        @property
        def can_be_used_at(cls, at):
            return at in cls.available
