from App import app, ViewNotLoadedYetError

class Section:
    @property
    def section_name(self) -> list:
        return self.getName()

    @property
    def append_prefix(self): # -> dict[str, int]
        return None

    def log(self, *args, **kwargs):
        _sections = self.section_name
        if kwargs.get('section') != None:
            _sections += kwargs.get('section')

        if kwargs.get("sections") != None:
            kwargs["section"] += kwargs.get("sections")
        if self.append_prefix != None:
            kwargs["prefix"] = self.append_prefix

        kwargs["section"] = _sections

        try:
            return app.Logger.log(*args, **kwargs)
        except ViewNotLoadedYetError:
            pass
        except AttributeError:
            pass
            #print("logger not initialized; ", args[0])
        except Exception as e:
            print("logger error; ", args[0])

    def log_error(self, *args, **kwargs):
        from App.Logger.LogKind import LogKindEnum

        kwargs["kind"] = LogKindEnum.error.value
        return self.log(*args, **kwargs)

    def log_success(self, *args, **kwargs):
        from App.Logger.LogKind import LogKindEnum

        kwargs["kind"] = LogKindEnum.success.value
        return self.log(*args, **kwargs)

    def fatal(self, exception):
        pass
