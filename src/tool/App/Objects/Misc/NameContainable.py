from App.Objects.Object import Object

class NameContainable(Object):
    def is_name_equals(self, name: str):
        return hasattr(self, 'name') and self.name == name

    def get_name_for_dictlist(self) -> str:
        return getattr(self, 'name')
