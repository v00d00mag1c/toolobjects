from Data.Explorer.ExplorerProtocol import ExplorerProtocol
from App.Objects.Arguments.ArgumentDict import ArgumentDict
from App.Objects.Arguments.Argument import Argument
from Data.Types.String import String
from App.Objects.Responses.ObjectsList import ObjectsList
from App.Storage.VirtualPath.Path import Path as VirtualPath
from App.DB.Search.Search import Search
from App import app

class Navigate(ExplorerProtocol):
    '''
    allows to view db items hierarchically as in file manager. Basically search wrapper
    '''

    @classmethod
    def _arguments(cls) -> ArgumentDict:
        return ArgumentDict(items = [
            Argument(
                name = 'path',
                orig = VirtualPath
            )
        ],
        missing_args_inclusion=True)

    async def _implementation(self, i):
        path = i.get('path')
        if path == None or path.has_parts() is False:
            _list = ObjectsList()
            for item in app.Storage.getAll():
                _list.append(item)

            return _list

        _vals = path.to_args().copy()
        _vals.update(i.values)

        _vals['storage'] = path.get_root().name
        _vals['public'] = True

        return await Search().execute(_vals)
