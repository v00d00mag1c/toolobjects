class ViewNotLoadedYetError(Exception):
    pass

class _Wrap:
    '''
    Allows to access the current view
    '''

    def __init__(self):
        self._view = None

    def mount(self, name: str, item):
        msg = f"Mounted {name} into globals"
        try:
            self.Logger.log(msg, role = ['objects_loading', 'objects_mounting'], section = ['Wrap'])
        except:
            pass

        # Not an Model, so we can attach any property
        setattr(self, name, item)

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

        if self._view == None:
            raise ViewNotLoadedYetError('view was not set yet')

        return getattr(self._view, name, None)

app = _Wrap()
