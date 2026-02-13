from App.Client.Displayment import Displayment
from Web.Bookmarks.Bookmark import Bookmark as RealBookmark
from App import app

class Bookmark(Displayment):
    for_object = 'App.Client.Bookmark'

    async def render_as_page(self, args = {}):
        url = self.request.rel_url.query.get('url')
        title = self.request.rel_url.query.get('title')
        collection = app.app.view._get_bookmarks_collection(self.auth)

        bookmark = RealBookmark(url = url)
        bookmark.obj.name = title
        collection.link(bookmark, role = ['internal'])

        bookmark.save()

        return self.redirect(url)
