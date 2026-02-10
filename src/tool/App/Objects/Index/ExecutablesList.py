from App.Objects.Object import Object
from pydantic import Field

class ExecutablesList(Object):
    '''
    All running executables
    '''

    items: list = Field()

    @classmethod
    def mount(cls):
        from App import app

        _objects = cls(
            items = []
        )

        app.mount('ExecutablesList', _objects)
