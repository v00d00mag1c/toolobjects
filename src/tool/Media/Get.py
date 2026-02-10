from App.Objects.ExtendedWheel import ExtendedWheel
from Data.Primitives.Collections.Collection import Collection
from App.Objects.Arguments.ArgumentDict import ArgumentDict
from App.Objects.Arguments.Argument import Argument
from App.Objects.Arguments.Assertions.NotNone import NotNone
from Data.Types.Boolean import Boolean
from Media.Media import Media
from App.Objects.Responses.Response import Response

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
        extract = self._get_submodule(i)
        collection = i.get('collection')
        if extract == None:
            self.log("Suitable submodule not found, calling _not_found_implementation()")

            return await self._not_found_implementation(i)

        _val = await extract.execute(i)
        if collection != None:
            for to_link in _val.getItems():
                collection.link(to_link)

        return _val
