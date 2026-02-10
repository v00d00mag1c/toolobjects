from App.Objects.Mixins.Model import Model
from pydantic import Field

class Geo(Model):
    lat: float = Field(default = None)
    long: float = Field(default = None)
