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
            for event in self.getEventsList():
                self.items[event] = []

        # TODO: move to decorator
        def check_category(self, category: str):
            assert category in self.getEventsList(), f"category \"{category}\" not in events list"

            if self.items.get(category) == None:
                self.items[category] = []

        @property
        def events(self) -> list:
            '''
            Every class must have "loaded" event. You must duplicate it every time :(
            '''
            return []

        def getEventsList(self) -> list:
            '''
            no, i've done workaround
            '''

            return self.events + ['loaded']

        def register(self):
            pass

        def get(self, category: str) -> list:
            self.check_category(category)

            return self.items.get(category)

        def run(self, hook_func: Callable, *args, **kwargs) -> None:
            if asyncio.iscoroutinefunction(hook_func):
                loop = asyncio.get_running_loop()
                task = loop.create_task(hook_func(*args, **kwargs))

            return hook_func(*args, **kwargs)

        def add(self, category: str, hook: Callable) -> None:
            self.check_category(category)
            self.items.get(category).append(hook)

        def remove(self, category: str, hook: Callable) -> None:
            self.check_category(category)
            self.items.get(category).remove(hook)

        # TODO: Add HookCategory class
        def trigger(self, category: str, *args, **kwargs) -> None:
            self.check_category(category)

            for hook in self.items.get(category):
                self.run(hook, *args, **kwargs)

        # TODO
        async def await_trigger(self, category: str, *args, **kwargs) -> None:
            self.trigger(category, *args, **kwargs)
