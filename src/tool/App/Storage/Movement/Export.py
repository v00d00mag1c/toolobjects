from App.Objects.Act import Act
from datetime import datetime
from App.Objects.Arguments.Assertions.NotNone import NotNone
from App.Objects.Arguments.ArgumentDict import ArgumentDict
from App.Objects.Arguments.Argument import Argument
from Data.Types.String import String
from Data.Types.Boolean import Boolean
from App.Objects.Responses.ObjectsList import ObjectsList
from App.Storage.Item.Create import Create
from App.Storage.Movement.Save import Save
from App.Storage.Item.Zip import Zip
from App.Objects.Relations.Submodule import Submodule

class Export(Act):
    @classmethod
    def _arguments(cls) -> ArgumentDict:
        return ArgumentDict(items = [
            Argument(
                name = 'items',
                assertions = [NotNone()],
                orig = ObjectsList
            ),
            Argument(
                name = 'name',
                default = None,
                orig = String
            ),
            Argument(
                name = 'dir',
                orig = String
            ),
            Argument(
                name = 'as_zip',
                default = False,
                orig = Boolean
            ),
            Argument(
                name = 'remove',
                default = True,
                orig = Boolean
            )
        ])

    @classmethod
    def _submodules(cls) -> list:
        return [
            Submodule(
                item = Create,
                role = ['usage']
            ),
            Submodule(
                item = Zip,
                role = ['usage']
            )
        ]

    async def _implementation(self, i):
        export_name = i.get("name")
        if export_name == None:
            export_name = f"{int(datetime.now().timestamp())}_export"

        _create_items = await Create().execute({
            'name': export_name,
            'dir': i.get('dir'),
            'mount': False
        })
        export_storage = _create_items.items[0]
        export_storage.is_export = True

        await Save().execute({
            'items': i.get('items'),
            'storage': [export_storage]
        })

        if i.get('as_zip') == True:
            await Zip().execute(i.update_values({
                'item': export_storage,
                'save_zip_to': i.get('dir')
            }).getValues())

        try:
            if i.get('remove'):
                export_storage.destroy()
        except Exception as e:
            self.log_error(e)

        return _create_items
