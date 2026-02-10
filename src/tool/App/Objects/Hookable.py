from pydantic import PrivateAttr
from typing import ClassVar, Any, Callable
from App import app
import asyncio

class Hookable():
    '''
    Allows to run subscribed functions at every event
    '''
    hooks: ClassVar[Any] = PrivateAttr(default = None)

    def init_subclass(cls):
        cls.hooks = cls._Hooks()

    class _Hooks:
        items: dict = {}

        def __init__(self):
            for event in self.events:
                self.items[event] = []

        # TODO: move to decorator
        def check_category(self, category: str):
            assert category in self.events, f"category \"{category}\" not in events list"

            if self.items.get(category) == None:
                self.items[category] = []

        @property
        def events(self) -> list:
            return []

        def register(self):
            pass

        def get(self, category: str) -> list:
            self.check_category(category)

            return self.items.get(category)

        def run(self, hook_func: Callable, *args, **kwargs) -> None:
            try:
                if asyncio.iscoroutinefunction(hook_func):
                    loop = asyncio.get_running_loop()
                    loop.create_task(hook_func(*args, **kwargs))
                else:
                    hook_func(*args, **kwargs)
            except Exception as e:
                self.log(str(e))

        def add(self, category: str, hook: Callable) -> None:
            self.check_category(category)

            self.items.get(category).append(hook)

        def remove(self, category: str, hook: Callable) -> None:
            self.check_category(category)

            try:
                self.items.get(category).remove(hook)
            except Exception:
                pass

        # TODO: Add HookCategory class
        def trigger(self, category: str, *args, **kwargs) -> None:
            self.check_category(category)

            for hook in self.items.get(category):
                self.run(hook, *args, **kwargs)
