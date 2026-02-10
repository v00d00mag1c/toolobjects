from App.Objects.Mixins.BaseModel import BaseModel
from pydantic import Field
from App import app

class Requirement(BaseModel):
    name: str = Field()
    version: str = Field(default = None)

    def get_name(self) -> str:
        if self.version != None:
            return f"{self.name}=={self.version}"

        return self.name

    def is_installed(self) -> bool:
        return self.name in app.app.installed_modules
