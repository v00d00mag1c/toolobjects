from App.Objects.Thumbnail import Thumbnail
from App.Objects.Arguments.ArgumentDict import ArgumentDict
from App.Objects.Arguments.Argument import Argument
from App.Objects.Arguments.Assertions.NotNone import NotNone
from App.Objects.Responses.ObjectsList import ObjectsList
from Media.Images.Image import Image
from Web.Pages.Page import Page
from App import app

class MakeScreenshot(Thumbnail):
    @classmethod
    def _arguments(cls) -> ArgumentDict:
        return ArgumentDict(items = [
            Argument(
                name = 'page',
                orig = Page,
                assertions = [NotNone()]
            )
        ])

    async def _implementation(self, i):
        thumbs = ObjectsList(items = [])
        page = i.get('page')

        for key in ['viewport', 'fullscreen']:
            try:
                self.log('making {0} screenshot...'.format(key))

                st = app.Storage.get('tmp').get_storage_adapter().get_storage_unit()
                filename = 'screenshot_' + key + '.png'

                path = st.get_root()
                new_path = path.joinpath(filename)

                st.setCommonFile(new_path)

                if key == 'viewport':
                    await page._page.get().screenshot(path=new_path)
                else:
                    await page._page.get().screenshot(
                        path = new_path,
                        full_page = True
                    )

                img = Image()
                img.set_storage_unit(st)
                img.save()

                thumbs.append(img)
            except Exception as e:
                self.log_error(e)

        return thumbs
