from Media.ByPath import ByPath
from App.Objects.Arguments.ArgumentDict import ArgumentDict
from App.Objects.Arguments.Argument import Argument
from App.Objects.Arguments.Assertions.NotNone import NotNone
from App.Objects.Object import Object
from Data.Types.String import String
from Data.Types.Int import Int
from Data.Types.Boolean import Boolean
from pathlib import Path

from App.Locale.Documentation import Documentation
from App.Locale.Key import Key

class ByPath(ByPath):
    @classmethod
    def _arguments(cls) -> ArgumentDict:
        return ArgumentDict(items = [
            Argument(
                name = 'object',
                default = 'Media.Text',
                orig = Object,
                assertions = [NotNone()]
            ),
            Argument(
                name = 'copy_file',
                default = True,
                orig = Boolean,
                documentation = Documentation(
                    name = Key(
                        value = 'Copy file'
                    ),
                    description = Key(
                        value = 'If True, it wouldn\'t set the `text` field and the text will be getting directly from file'
                    )
                )
            ),
            Argument(
                name = 'encoding',
                default = 'utf-8',
                orig = String
            ),
            Argument(
                name = 'split_by',
                orig = String,
                default = None
            ),
            Argument(
                name = 'split_by.limit',
                orig = Int,
                default = None
            )
        ])

    def _get_objects(self, i, item):
        encoding = i.get('encoding')
        copy_file = i.get('copy_file')
        separator = i.get('split_by')
        separator_limit = i.get('split_by.limit')

        text_value = Path(item).read_text(encoding = encoding)
        texts = []

        if separator != None and copy_file == False:
            if separator_limit:
                texts = text_value.split(separator, separator_limit)
            else:
                texts = text_value.split(separator)
        else:
            texts = [text_value]

        storage_unit = None
        if copy_file:
            storage_unit = self._move_file(item, i)

        for text in texts:
            obj = i.get('object')()
            if copy_file == False:
                obj.value = text
                obj.has_set_from_file = True
            else:
                obj.set_storage_unit(storage_unit)

            yield obj
