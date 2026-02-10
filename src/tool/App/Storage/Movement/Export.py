from App.Objects.Act import Act
from datetime import datetime
from App.Storage.StorageItem import StorageItem
from App.Arguments.ArgumentDict import ArgumentDict
from App.Arguments.Types.String import String
from App.Arguments.Objects.Orig import Orig
from App.Arguments.Types.Boolean import Boolean
from App.Arguments.Assertions.NotNoneAssertion import NotNoneAssertion
from App.Responses.ObjectsList import ObjectsList
from App.Responses.AnyResponse import AnyResponse

class Export(Act):
    '''
    Creates new StorageItem, moves items to it
    '''

    @classmethod
    def getArguments(cls) -> ArgumentDict:
        return ArgumentDict(items = [
            Orig(
                name = 'items',
                orig = ObjectsList
            ),
            String(
                name = 'export_name',
                default = None
            ),
            String(
                name = 'dir',
                assertions = [NotNoneAssertion()]
            ),
            Boolean(
                name = 'as_zip',
                default = False
            )
        ])

    async def implementation(self, i):
        self.log('Exporting')

        export_name = i.get("export_name")
        if export_name == None:
            export_name = f"{int(datetime.now().timestamp())}_export"

        news = StorageItem(
            name = export_name,
            directory = str(i.get('dir')),
            db = {
                'adapter': 'sqlite'
            }
        )

        self.log(f"Created new StorageItem {export_name}, dir is {str(i.get('dir'))}")

        for item in i.get('items').getItems():
            item.flush(news)

            self.log(f"flushed item to db {export_name}, uuid: {item.getDbId()}")

        return AnyResponse.fromItems(news.directory)
