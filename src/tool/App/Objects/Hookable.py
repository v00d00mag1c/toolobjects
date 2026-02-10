from pydantic import Field
from typing import ClassVar, Any, Callable
from App import app
import asyncio

class Hookable():
    '''
    Allows to run subscribed functions at every event
    '''
    _hooks: dict[str, list] = {}

    @classmethod
    def getClassEventsTypes(cls):
        '''
        events of each class
        '''
        return []

    def constructor(self):
        super().constructor()

        self._hooks = {}

        for event in self.getClassEventsTypes():
            self._hooks[event] = []

    def checkEventType(self, category: str):
        assert category in self.getClassEventsTypes(), f"category \"{category}\" not in events list"

        if self._hooks.get(category) == None:
            self._hooks[category] = []

    def getEvent(self, category: str) -> list:
        self.checkEventType(category)

        return self._hooks.get(category)

    def runHook(self, hook_func: Callable, *args, **kwargs) -> None:
        if asyncio.iscoroutinefunction(hook_func):
            return app.app.hook_thread.task_queue.put((hook_func, args, kwargs))

        return hook_func(*args, **kwargs)

    def addHook(self, category: str, hook: Callable) -> None:
        self.checkEventType(category)
        self._hooks.get(category).append(hook)

    def removeHook(self, category: str, hook: Callable) -> None:
        self.checkEventType(category)
        self._hooks.get(category).remove(hook)

    # TODO: Add HookCategory class
    def triggerHooks(self, category: str, *args, **kwargs) -> None:
        self.checkEventType(category)

        for hook in self._hooks.get(category):
            self.runHook(hook, *args, **kwargs)

    # TODO
    async def awaitTriggerHooks(self, category: str, *args, **kwargs) -> None:
        self.triggerHooks(category, *args, **kwargs)
