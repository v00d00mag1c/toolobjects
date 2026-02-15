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
from App.Locale.Documentation import Documentation
from App.Locale.Key import Key

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
                default = True,
                documentation = Documentation(
                    name = Key(
                        value = 'Split folders on collections'
                    ),
                    description = Key(
                        value = 'False: Every file will be added to single collection.\nTrue: Every folder will represent collection with their files'
                    )
                )
            ),
            Argument(
                name = 'split.collection_type',
                orig = Object,
                default = 'Media.List.List'
            ),
            Argument(
                name = 'split.find_covers',
                orig = Boolean,
                default = True
            ),
            ListArgument(
                name = 'split.find_covers.extensions',
                orig = String,
                default = []
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
        assert self.getOption('app.permissions.file_access') == True, 'access denied'

        allowed_extensions = i.get('allowed_extensions')
        find_covers = i.get('split.find_covers')
        find_covers_ext = i.get('split.find_covers.extensions')
        do_split = i.get('split')
        collection_type = i.get('split.collection_type')
        if collection_type is None:
            collection_type = Collection

        max_depth = i.get('dir_max_depth')
        if len(allowed_extensions) == 0:
            allowed_extensions = i.get('object').extensions
        if len(find_covers_ext) == 0:
            find_covers_ext = i.get('object').cover_extensions
        if len(allowed_extensions) == 0:
            allowed_extensions = None
        if len(find_covers_ext) == 0:
            find_covers_ext = None
        pathes_collections = dict()

        def check_suffix(path):
            for suffix in path.suffixes:
                _suf = suffix.lower()[1:]

                if allowed_extensions != None:
                    if _suf in allowed_extensions:
                        return True
                else:
                    return True

            return False

        def check_cover(path):
            for suffix in path.suffixes:
                _suf = suffix.lower()[1:]

                if find_covers_ext != None:
                    if _suf in find_covers_ext:
                        return True
                else:
                    return False

            return False

        async def rglob(path, pattern, max_depth, current_depth = 0, old_coll = None) -> Generator:
            pathes = {'path': path, 'coll': None, 'old_path': old_coll, 'items': list(), 'name': path.name}
            # Split is enabled, so creating collection for the current level
            coll = None
            covers = list()
            if do_split:
                coll = collection_type()
                # Assigning it the name of the folder
                coll.obj.name = path.name
                coll.local_obj.make_public()
                pathes['coll'] = coll

                self.log('split to new collection (name: {0})'.format(coll.obj.name))

                #pathes_collections[str(path)] = coll
                self.append(coll)

                if old_coll != None:
                    old_coll.link(coll)

            for item in path.glob(pattern):
                new_path = Path(item)

                if find_covers:
                    if check_cover(new_path):
                        covers.append(new_path)

                if new_path.is_dir():
                    async for _y_item in rglob(new_path, pattern, max_depth, current_depth + 1, coll):
                        yield _y_item

                if check_suffix(new_path) == False:
                    continue

                pathes['items'].append(str(new_path))

            if coll != None:
                for cover_item in covers:
                    self.log('found cover item {0}'.format(str(cover_item)))

                    try:
                        for _item in await i.get('object').get_thumbnail_for_collection(cover_item):
                            coll.add_thumbnail(_item)
                    except Exception as e:
                        self.log_error(e)

            yield pathes

        # Passed paths
        for dir_item in i.get('dir'):
            self.log('Path {0}'.format(dir_item))

            # Iterating subfolders
            async for item in rglob(dir_item, '*', max_depth):
                self.log('Subpath {0}'.format(item.get('path')))

                # Getting as ByPath
                _execute_vals = i.getValues()
                _execute_vals['set_info'] = True
                _execute_vals['path'] = item.get('items')

                vals = await i.get('object')._get_submodule_by_last('ByPath')().execute(_execute_vals)
                coll = item.get('coll')

                for item in vals.getItems():
                    if coll:
                        coll.link(item, role = ['list_item'])
                    else:
                        self.append(item)

                    item.local_obj.make_public()
