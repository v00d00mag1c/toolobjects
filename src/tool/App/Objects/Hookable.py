from pydantic import Field
from typing import ClassVar, Any, Callable
from App import app
import asyncio

class Hookable():
    '''
    Allows to run subscribed functions at every event
    '''
    hooks: dict[str, list] = Field(default = {})

    @classmethod
    def getClassEventsTypes(cls):
        '''
        events of each class
        '''
        return []

    def constructor(self):
        super().constructor()

        self.hooks = {}

        for event in self.getClassEventsTypes():
            self.hooks[event] = []

    def checkEventType(self, category: str):
        assert category in self.getClassEventsTypes(), f"category \"{category}\" not in events list"

        if self.hooks.get(category) == None:
            self.hooks[category] = []

    def getEvent(self, category: str) -> list:
        self.checkEventType(category)

        return self.hooks.get(category)

    def runHook(self, hook_func: Callable, *args, **kwargs) -> None:
        if asyncio.iscoroutinefunction(hook_func):
            app.app.hook_thread.task_queue.put((hook_func, args, kwargs))

            #task = app.app.loop.create_task(hook_func(*args, **kwargs))
            #app.app.loop.call_soon(lambda: None)

        return hook_func(*args, **kwargs)

    def addHook(self, category: str, hook: Callable) -> None:
        self.checkEventType(category)
        self.hooks.get(category).append(hook)

    def removeHook(self, category: str, hook: Callable) -> None:
        self.checkEventType(category)
        self.hooks.get(category).remove(hook)

    # TODO: Add HookCategory class
    def triggerHooks(self, category: str, *args, **kwargs) -> None:
        self.checkEventType(category)

        for hook in self.hooks.get(category):
            self.runHook(hook, *args, **kwargs)

    # TODO
    async def awaitTriggerHooks(self, category: str, *args, **kwargs) -> None:
        self.triggerHooks(category, *args, **kwargs)
