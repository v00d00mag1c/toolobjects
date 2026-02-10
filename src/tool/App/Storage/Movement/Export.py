from App.Objects.Act import Act
from datetime import datetime
from App.Storage.StorageItem import StorageItem
from App.Objects.Arguments.ArgumentDict import ArgumentDict
from App.Objects.Arguments.Argument import Argument
from Data.String import String
from Data.Int import Int
from Data.Boolean import Boolean
from App.Objects.Arguments.Assertions.NotNoneAssertion import NotNoneAssertion
from App.Responses.ObjectsList import ObjectsList
from App.Responses.AnyResponse import AnyResponse

class Export(Act):
    '''
    Creates new StorageItem, moves items to it
    '''

    @classmethod
    def getArguments(cls) -> ArgumentDict:
        return ArgumentDict(items = [
            Argument(
                name = 'items',
                orig = ObjectsList
            ),
            Argument(
                name = 'export_name',
                default = None,
                orig = String
            ),
            Argument(
                name = 'dir',
                assertions = [NotNoneAssertion()],
                orig = String
            ),
            Argument(
                name = 'as_zip',
                default = False,
                orig = Boolean
            ),
            Argument(
                name = 'link_max_depth',
                default = 10, # TODO move to const
                orig = Int
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

        if i.get('as_zip') == True:
            self.log('not implemented')

        return AnyResponse.fromItems(news)
