# Initialization file

from App.App import App
from App.Views.View import View
#import tracemalloc
#tracemalloc.start()

current = App()
current._constructor()

async def _main():
    tmp_view = View(app = current)
    tmp_view.setAsCommon()

    current.load_plugins(current.cwd)

    view_name = current.argv.get('view', 'App.Console.Console.Console')
    view_class = current.objects.getByName(view_name)
    view = view_class.module()
    view.setAsCommon()
    view.setApp(current)

    await view.execute(current.argv)

current.loop.run_until_complete(_main())
