from App import app

class Section:
    @property
    def section_name(self) -> list:
        # it implies that you have extended Object
        return self.meta.name

    @property
    def append_prefix(self): # -> LogPrefix
        return None

    def log(self, *args, **kwargs):
        kwargs["section"] = self.section_name
        if kwargs.get("sections") != None:
            kwargs["section"] += kwargs.get("sections")

        if self.append_prefix != None:
            kwargs["prefix"] = self.append_prefix

        try:
            return app.Logger.log(*args, **kwargs)
        except:
            print_before_init = True
            if print_before_init == True:
                print(args[0])

    def log_error(self, *args, **kwargs):
        from Plugins.App.Logger.LogParts.LogKind import LogKindEnum

        kwargs["kind"] = LogKindEnum.error.value
        return self.log(*args, **kwargs)

    def log_success(self, *args, **kwargs):
        from Plugins.App.Logger.LogParts.LogKind import LogKindEnum

        kwargs["kind"] = LogKindEnum.success.value
        return self.log(*args, **kwargs)
