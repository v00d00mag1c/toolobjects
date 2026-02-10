from App.Objects.ExtendedWheel import ExtendedWheel
from Data.Primitives.Collections.Collection import Collection
from App.Objects.Arguments.ArgumentDict import ArgumentDict
from App.Objects.Arguments.Argument import Argument
from App.Objects.Arguments.Assertions.NotNone import NotNone
from App.Objects.Responses.ObjectsList import ObjectsList
from App.Objects.Responses.Response import Response
from Data.Types.Boolean import Boolean
from Media.Media import Media

class Get(ExtendedWheel):
    @classmethod
    def _arguments(cls) -> ArgumentDict:
        return ArgumentDict(items = [
            Argument(
                name = 'object',
                orig = Media,
                assertions = [NotNone()]
            ),
            Argument(
                name = 'public',
                orig = Boolean,
                default = True
            ),
            Argument(
                name = 'collection',
                by_id = True,
                orig = Collection
            ),
            Argument(
                name = 'make_thumbnail',
                default = False,
                orig = Boolean
            )
        ], missing_args_inclusion = True)

    async def _implementation(self, i) -> Response:
        _obj = i.get('object')
        extract = self._get_submodule(i)
        collection = i.get('collection')
        if extract == None:
            self.log("Suitable submodule not found, calling _not_found_implementation()")

            return await self._not_found_implementation(i)

        _val = await extract.execute(i)
        _thumbnails = list()
        for thumb in _obj.getSubmodules():
            if 'thumbnail' in thumb.role:
                _thumbnails.append(thumb)

        has_collection = collection != None
        _it = 0

        for item in _val.getItems():
            if has_collection == True:
                collection.link(item)

            if i.get('public'):
                item.local_obj.make_public()

            if i.get('make_thumbnail') == True:
                for thumb_func in _thumbnails:
                    try:
                        _resp = await thumb_func.item().execute({
                            'object': item
                        })
                        item.local_obj.add_thumbnails(_resp.getItems())

                        self.log('thumbnail for item {0}: done'.format(_it))
                    except Exception as e:
                        self.log_error(e, role = ['thumbnail'], exception_prefix = 'Error when making thumbnail: ')

            _it += 1

        return _val
