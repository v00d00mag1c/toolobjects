class _Wrap:
    '''
    Allows to access the current view
    '''

    def __init__(self):
        self._view = None

    def mount(self, name, item):
        setattr(self._view.app.app, name, item)

    def setView(self, view):
        '''
        Sets the global view and app that can be accessed via

        from App import app
        '''

        self._view = view

    def __getattr__(self, name):
        '''
        Allows to use mounted singltones

        app.Logger.log(...)
        '''

        if name == "settings":
            return self._view.app.app.settings

        return getattr(self._view.app.app, name, None)

app = _Wrap()
