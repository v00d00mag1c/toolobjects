from Data.Explorer.ExplorerProtocol import ExplorerProtocol
from App.Objects.Arguments.Assertions.NotNoneAssertion import NotNoneAssertion
from App.Objects.Arguments.ArgumentDict import ArgumentDict
from App.Objects.Arguments.Argument import Argument
from Data.String import String
from App.Objects.Responses.ObjectsList import ObjectsList
from App.Storage.VirtualPath.Path import Path as VirtualPath
from App import app

class Navigate(ExplorerProtocol):
    '''
    Navigates by db

    path format: db:/item1/item2
    '''

    @classmethod
    def _arguments(cls) -> ArgumentDict:
        return ArgumentDict(items = [
            Argument(
                name = 'path',
                orig = String
            )
        ])

    async def implementation(self, i):
        _path = i.get('path')
        if _path == None:
            _list = ObjectsList()
            for item in app.Storage.getAll():
                _list.append(item)

            return _list

        path = VirtualPath.from_str(_path)
        print(path)

        #return path.getContent()
