from App.App import App

current = App()
current._constructor()
current.load_plugins(current.cwd)
