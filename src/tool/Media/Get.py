from App.Objects.ExtendedWheel import ExtendedWheel
from Data.Primitives.Collections.Collection import Collection
from App.Objects.Arguments.ArgumentDict import ArgumentDict
from App.Objects.Arguments.Argument import Argument
from App.Objects.Arguments.ListArgument import ListArgument
from App.Objects.Arguments.Assertions.NotNone import NotNone
from App.Objects.Responses.ObjectsList import ObjectsList
from App.Objects.Responses.Response import Response
from Data.Types.Boolean import Boolean
from Data.Types.String import String
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
            ListArgument(
                name = 'thumbnails',
                default = ['*'],
                orig = String
            )
        ], missing_args_inclusion = True)

    async def _implementation(self, i) -> Response:
        _obj = i.get('object')
        extract = self._get_submodule(i)
        if extract == None:
            self.log("Suitable submodule not found, calling _not_found_implementation()")

            return await self._not_found_implementation(i)

        # Extraction of found module
        _val = await extract.execute(i)

        # Thumbnails

        allowed_thumbnails = [] # If None, runs every thumbnail submodule
        for item in i.get('thumbnails'):
            if item == '*':
                allowed_thumbnails = None
                break

            allowed_thumbnails.append(item)

        # Creating the list of thumbnail methods

        thumbnails_methods = list()
        for thumb in _obj.getSubmodules():
            if 'thumbnail' in thumb.role:
                _is_current_allowed = False
                if allowed_thumbnails != None:
                    for allowed in allowed_thumbnails:
                        if thumb.item.is_same_name(allowed):
                            _is_current_allowed = True
                else:
                    _is_current_allowed = True

                if _is_current_allowed == True:
                    thumbnails_methods.append(thumb)

        item_count = 0
        for item in _val.getItems():
            if i.get('public'):
                item.local_obj.make_public()

            for thumb_func in thumbnails_methods:
                try:
                    _item = thumb_func.item
                    _resp = await _item().execute({
                        'object': item
                    })
                    item.local_obj.add_thumbnails(_resp.getItems())

                    self.log('thumbnail for item {0}, {1}'.format(item_count, _item._getNameJoined()), role = ['thumbnail'])
                except Exception as e:
                    self.log_error(e, role = ['thumbnail'], exception_prefix = 'Error when making thumbnail: ')

            item_count += 1

        return _val
