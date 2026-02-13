from App.Objects.Object import Object
from pydantic import Field

class URL(Object):
    url: str = Field(default = None)
    main_url: str = Field(default = 'https://youtube.com/watch?v=')
    timecode: int | float = Field(default = None)
