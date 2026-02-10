from pydantic import BaseModel, Field
from typing import Any

class LinkInsertion(BaseModel):
    link: Any = Field()
    field: list[str] = Field(default = [])

    def unwrap(self):
        _item = getattr(self.link, 'item')

        if len(self.field) > 0:
            _main_item = _item
            for link in self.field:
                _main_item = getattr(_main_item, link, None)

            return _main_item

        return _item
