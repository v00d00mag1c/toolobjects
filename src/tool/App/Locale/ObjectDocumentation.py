from App.Locale.Documentation import Documentation
from App.Locale.Key import Key
from pydantic import Field

class ObjectDocumentation(Documentation):
    fields: dict[str, Key] = Field(default = {})
