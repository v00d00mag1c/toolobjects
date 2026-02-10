from Data.Explorer.ExplorerProtocol import ExplorerProtocol
from App.Objects.Responses.ObjectsList import ObjectsList
from pathlib import Path
from App.Objects.Arguments.ArgumentDict import ArgumentDict
from App.Objects.Arguments.Argument import Argument
from App.Objects.Arguments.Assertions.NotNoneAssertion import NotNoneAssertion
from Data.String import String

from Media.Files.File import File
from Media.Files.Dir import Dir
from App.Objects.Relations.Submodule import Submodule

class Explorer(ExplorerProtocol):
    @classmethod
    def _submodules(cls):
        return [
            Submodule(
                item = Dir,
            ),
            Submodule(
                item = File,
            )
        ]

    @classmethod
    def _arguments(cls) -> ArgumentDict:
        return ArgumentDict(items = [
                Argument(
                    name = 'path',
                    orig = String,
                    assertions = [NotNoneAssertion()]
                )
            ],
            missing_args_inclusion = True
        )

    async def implementation(self, i):
        _list = ObjectsList(items = [])

        _path = Path(str(i.get('path')))
        _item = File.from_path(_path)

        _list.items = _item.get_file().get_content()

        return _list
