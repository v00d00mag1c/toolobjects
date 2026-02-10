from App.Objects.Object import Object
from typing import ClassVar
from App import app

class Migrated(Object):
    '''
    Link to another object.
    '''

    is_migration: ClassVar[bool] = True
    migrated_to: ClassVar[str] = '' # Change this

    @classmethod
    def get_migrated_to(cls, content: dict) -> str:
        return app.ObjectsList.getByName(cls.migrated_to).getModule()
