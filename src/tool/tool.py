# Entry point

from App.App import App
#import tracemalloc
#tracemalloc.start()

current = App()
current.loop.run_until_complete(current.runView(current.loadView()))
