from App.Objects.Act import Act
from App.Objects.Arguments.ArgumentDict import ArgumentDict
from App.Objects.Arguments.Argument import Argument
from App.Objects.Arguments.Assertions.NotNone import NotNone

from Data.Types.Boolean import Boolean
from Data.Types.String import String

from App.Objects.Index.Namespaces.Namespace import Namespace
from App import app

class Add(Act):
    @classmethod
    def _arguments(cls) -> ArgumentDict:
        return ArgumentDict(items = [
            Argument(
                name = 'name',
                orig = String
            ),
            Argument(
                name = 'add_path',
                orig = String
            ),
            Argument(
                name = 'to_config',
                orig = Boolean,
                default = True
            ),
            Argument(
                name = 'add_to_current',
                orig = Boolean,
                default = False
            ),
            Argument(
                name = 'confirm',
                orig = Boolean,
                default = False
            )
        ])

    @staticmethod
    def check_confirm(val: bool):
        assert val == True, 'The installed plugins will have full access to your system. If you trust these files, set the \'confirm\' as true'

    def _implementation(self, i):
        assert True, 'FromDir or FromZip'

    def _install(self, i):
        _name = i.get('name')

        assert app.ObjectsList.has_namespace_with_name(_name) == False, 'Namespace with name {0} already exists'.format(_name)

        _new = Namespace(
            root = i.get('add_path'),
            name = _name
        )
        _new.load()

        app.ObjectsList.namespaces.append(_new)

        self.log('added namespace {0}'.format(_name))

        if i.get('to_config') == True:
            _conf_val = app.Config.getItem().get('objects.index.namespaces', raw = True)
            if _conf_val == None:
                _conf_val = []
            _conf_val.append(_new.to_minimal_json())

            app.Config.getItem().set('objects.index.namespaces', _conf_val)

            if i.get('add_to_current') == True:
                _conf_val2 = app.Config.getItem().get('objects.index.namespaces.current', raw = True)
                if _conf_val2 == None:
                    _conf_val2 = []
                _conf_val2.append(_new.name)

                app.Config.getItem().set('objects.index.namespaces.current', _conf_val)
