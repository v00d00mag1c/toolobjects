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
from Data.Types.Dict import Dict
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
            ListArgument(
                name = 'thumbnails',
                default = ['*'],
                orig = String
            ),
            Argument(
                name = 'thumbnail_settings', # Args for each thumbnail
                orig = Dict,
                default = {}
            )
        ], missing_args_inclusion = True)

    async def _implementation(self, i) -> Response:
        _obj = i.get('object')
        thumbnail_settings = i.get('thumbnail_settings')
        extract = self._get_submodule(i)
        if extract == None:
            self.log("Suitable submodule not found, calling _not_found_implementation()")

            return await self._not_found_implementation(i)

        # Extraction of found module
        _val = await extract.execute(i)

        # Getting the list of allowed thumbnails
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
                is_current_allowed = False
                if allowed_thumbnails != None:
                    for allowed in allowed_thumbnails:
                        if thumb.item.is_same_name(allowed):
                            is_current_allowed = True
                else:
                    is_current_allowed = 'thumbnail_disabled_default' not in thumb.role

                if is_current_allowed == True:
                    thumbnails_methods.append(thumb)

        item_count = 0
        for _item in _val.getItems():
            iterate_objects = list()
            if _item.isInMRO(Media) == False:
                for _item_obj in _item.getLinked():
                    iterate_objects.append(_item_obj.getItem())
            else:
                iterate_objects = [_item]

            for item in iterate_objects:
                for thumb_func in thumbnails_methods:
                    thumb_item = thumb_func.getItem()
                    current_thumbnail_settings = {}
                    if thumb_item._getNameJoined() in thumbnail_settings:
                        current_thumbnail_settings.update(thumbnail_settings.get(thumb_item._getNameJoined()))

                    current_thumbnail_settings.update({
                        'object': item
                    })

                    try:
                        _resp = await thumb_item().execute(current_thumbnail_settings)

                        for thumb_result in _resp.getItems():
                            item.add_thumbnail(thumb_result)

                        self.log('thumbnail for item {0}, {1}'.format(item_count, thumb_item._getNameJoined()), role = ['thumbnail'])
                    except Exception as e:
                        self.log_error(e, role = ['thumbnail'], exception_prefix = 'thumbnail for item {0}, {1}: '.format(item_count, thumb_item._getNameJoined()))

                item_count += 1

        return _val
