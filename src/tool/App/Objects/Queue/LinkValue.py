from App.Objects.Object import Object
from pydantic import Field

class LinkValue(Object):
    value: str = Field()

    def toString(self, prestart: dict, items: list):
        _items: list[str] = self.value.split(".")
        applied_parts: list = []

        self.log(f"Checking string {self.value}")

        RETURN_INDEX = -1
        ITEMS_MODIFIER = '#'
        PRESTART_MODIFIER = '$'

        # TODO: rewrite to func
        for i in range(0, len(_items)):

            item = _items[i]
            prev = None
            if i > 0:
                prev = applied_parts[i - 1]

            self.log(f"part {i}: {item} with previous = {prev}")

            if item.startswith(ITEMS_MODIFIER):
                ids = int(item.replace(ITEMS_MODIFIER, ''))

                self.log(f"str {i}: {item} is link to items")

                applied_parts.append(items[ids])
            elif item.startswith(PRESTART_MODIFIER):
                ids = int(item.replace(PRESTART_MODIFIER, ''))

                self.log(f"str {i}: {item} is link to prestart")

                applied_parts.append(prestart[ids])
            if type(prev) == dict:
                self.log(f"str {i}: {item} is a key")

                applied_parts.append(prev[item])
            elif type(prev) == list:
                self.log(f"str {i}: {item} is an index")

                try:
                    applied_parts.append(prev[int(item)])
                except IndexError as e:
                    self.log(f"str {i}: arr does not contains index {item}")
                    self.fatal(e)
            elif hasattr(prev, item):
                self.log(f"str {i}: {item} is a key to object")

                applied_parts.append(getattr(prev, item))

        self.log(f"{_items} >>> {applied_parts}")

        return applied_parts[RETURN_INDEX]
