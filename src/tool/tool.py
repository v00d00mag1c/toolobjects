# Initialization file

from App.App import App
from App.Views.View import View

current = App()
tmp_view = View(app = current)
tmp_view.setAsCommon()

current._constructor()
current.load_plugins(current.cwd)

view_name = current.argv.get('view', 'App.Console.Console.Console')
view_class = current.objects.getByName(view_name)
view = view_class.module()
view.setAsCommon()
view.setApp(current)
current.loop.run_until_complete(view.execute(current.argv))
