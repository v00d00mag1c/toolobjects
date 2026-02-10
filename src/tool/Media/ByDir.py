from App.Objects.Extractor import Extractor
from App.Objects.Arguments.ArgumentDict import ArgumentDict
from App.Objects.Arguments.Argument import Argument
from App.Objects.Arguments.ListArgument import ListArgument
from App.Objects.Arguments.Assertions.NotNone import NotNone
from App.Objects.Object import Object
from Media.Files.FilePath import FilePath
from Data.Types.Boolean import Boolean
from Data.Types.String import String
from Data.Types.Int import Int
from typing import Generator
from pathlib import Path

from Media.ByPath import ByPath
from Data.Primitives.Collections.Collection import Collection

class ByDir(Extractor):
    @classmethod
    def _arguments(cls) -> ArgumentDict:
        return ArgumentDict(items = [
            ListArgument(
                name = 'dir',
                orig = FilePath,
                assertions = [NotNone()]
            ),
            Argument(
                name = 'split',
                orig = Boolean,
                default = False
            ),
            Argument(
                name = 'split.collection_type',
                orig = Object,
                default = 'Data.Primitives.Collections.Collection'
            ),
            ListArgument(
                name = 'allowed_extensions',
                orig = String,
                default = None
            ),
            Argument(
                name = 'dir_max_depth',
                orig = Int,
                default = 10
            )
        ]).join_class(ByPath, only = ['object', 'symlink', 'set_source'])

    async def _implementation(self, i):
        allowed_extensions = i.get('allowed_extensions')
        do_split = i.get('split')
        collection_type = i.get('split.collection_type')
        if collection_type is None:
            collection_type = Collection

        max_depth = i.get('dir_max_depth')
        if len(allowed_extensions) == 0:
            allowed_extensions = i.get('object').extensions
        if len(allowed_extensions) == 0:
            allowed_extensions = None

        def check_suffix(path):
            for suffix in path.suffixes:
                _suf = suffix.lower()[1:]

                if allowed_extensions != None:
                    if _suf in allowed_extensions:
                        return True
                else:
                    return True

            return False

        def rglob(path, pattern, max_depth, current_depth = 0) -> Generator:
            pathes = {'items': list(), 'name': path.name}
            for item in path.glob(pattern):
                path = Path(item)
                if path.is_dir():
                    yield from rglob(path, pattern, max_depth, current_depth + 1)

                if check_suffix(path) == False:
                    continue

                pathes.get('items').append(str(path))

            yield pathes

        for dir_item in i.get('dir'):
            for item in rglob(dir_item, '*', max_depth):
                _vals = i.getValues()
                _vals['path'] = item.get('items')

                vals = await ByPath().execute(_vals)
                coll = None
                if do_split:
                    coll = collection_type()
                    coll.obj.name = item.get('name')
                    self.append(coll)

                for item in vals.getItems():
                    if coll:
                        coll.link(item, role = ['list_item'])
                    else:
                        self.append(item)
