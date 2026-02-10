from Data.Primitives.Collections.Create import Create as RealCreate
from App.Objects.Arguments.ArgumentDict import ArgumentDict
from App.Objects.Arguments.ListArgument import ListArgument
from Data.Types.String import String

class Create(RealCreate):
    type_that_creates = 'Media.List.List'

    @classmethod
    def _arguments(cls) -> ArgumentDict:
        return ArgumentDict(items = [
            ListArgument(
                name = 'media_types',
                orig = String,
            )
        ])

    def _creation_hook(self, collection, i):
        collection.media_types = i.get('media_types')
