from App.Objects.Extractor import Extractor
from App.Objects.Object import Object
from App.Objects.Arguments.Argument import Argument
from App.Objects.Arguments.ArgumentDict import ArgumentDict
from Data.Types.Dict import Dict
from App import app

class Create(Extractor):
    @classmethod
    def _arguments(cls) -> ArgumentDict:
        return ArgumentDict(items = [
            Argument(
                name = 'prototype',
                orig = Object,
                default = 'App.Objects.Misc.Abstract'
            ),
            Argument(
                name = 'fields',
                orig = Dict,
                default = {}
            )
        ])

    async def _implementation(self, i):
        prototype = i.get('prototype')
        fields = i.get('fields')
        assert prototype != None, 'prototype not found'

        obj = prototype()
        for key, val in fields.items():
            _u_object = obj

            try:
                splitted = key.split('.')
                for _key in splitted:
                    if splitted[-1] == _key:
                        setattr(_u_object, _key, val)
                    else:
                        _u_object = getattr(_u_object, _key, None)
            except Exception as e:
                self.log_error(e)

        self.append(obj)
