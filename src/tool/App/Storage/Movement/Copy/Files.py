from App.Objects.Act import Act
from App.Objects.Arguments.ArgumentDict import ArgumentDict
from App.Objects.Arguments.Argument import Argument
from App.Objects.Arguments.LiteralArgument import LiteralArgument
from App.Objects.Responses.ObjectsList import ObjectsList
from App.Objects.Arguments.Assertions.NotNoneAssertion import NotNoneAssertion
from Data.String import String
from pathlib import Path
import shutil, datetime

class Files(Act):
    @classmethod
    def _arguments(cls) -> ArgumentDict:
        return ArgumentDict(items = [
            Argument(
                name = 'items',
                orig = ObjectsList,
                assertions = [NotNoneAssertion()]
            ),
            Argument(
                name = 'directory',
                orig = String,
                assertions = [NotNoneAssertion()]
            ),
            LiteralArgument(
                values = ['{0}.{1}', '{0}_{2}.{1}', '{0}_{3}.{1}'],
                strict = False,
                name = 'save_format',
                orig = String,
                default = '{0}_{3}.{1}'
            )
        ])

    async def implementation(self, i):
        _items = i.get('items')
        _directory = Path(i.get('directory'))

        for storage_unit in _items.getItems():
            for file in storage_unit.getFiles():
                _now = datetime.datetime.now().timestamp()
                _new_name = _directory.joinpath(i.get('save_format').format(
                    file.get_name_only(), # 0
                    file.ext, # 1
                    storage_unit.hash, # 2
                    int(_now), # 3
                    storage_unit.getDbId()) # 4
                )

                shutil.copy(file.getPath(), str(_new_name))
