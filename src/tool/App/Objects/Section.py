from App import app, ViewNotLoadedYetError

class Section:
    '''
    Adds to Object logger shortcuts
    '''

    @property
    def section_name(self) -> list:
        '''
        Section that will be appended to Log.
        Its taken to "property" to allow to override
        '''
        return self.getName()

    @property
    def append_prefix(self): # -> dict[str, int]
        '''
        Thing that shows id of some object like:

        DownloadItem->1
        '''
        return None

    def log_shortcut(self, *args, _role = [], **kwargs):
        _sections = self.section_name
        if self.append_prefix != None:
            kwargs["prefix"] = self.append_prefix
        if kwargs.get('section') != None:
            _sections += kwargs.get('section')
        if kwargs.get('role') == None:
            kwargs['role'] = []
        for role in _role:
            kwargs['role'].append(role)

        kwargs["section"] = _sections
        try:
            return app.Logger.log(*args, **kwargs)
        except ViewNotLoadedYetError:
            pass
        except AttributeError:
            pass
        except Exception as e:
            raise (e)
            self.log_raw("logger error; ", args[0])

    def log(self, *args, **kwargs):
        return self.log_shortcut(*args, **kwargs)

    def log_error(self, *args, **kwargs):
        return self.log_shortcut(*args, _role=['error'], **kwargs)

    def log_success(self, *args, **kwargs):
        return self.log_shortcut(*args, _role=['success'], **kwargs)

    def log_raw(self, anything: str):
        '''
        Just an alias for "print()". XD!!!!!!!!!
        Everything (except ObjectAdapters) is an objects, so this function will be available everywhere.
        '''
        print(anything)

    def fatal(self, exception):
        raise exception
