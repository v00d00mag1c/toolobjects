from App.Objects.Object import Object
from App.Objects.Threads.ExecutionThread import ExecutionThread
from pydantic import Field
from collections import deque
from typing import Generator
from App import app

class ThreadsList(Object):
    '''
    All running threads
    '''

    items: deque = Field()

    @classmethod
    def mount(cls):
        from App import app

        _objects = cls(
            items = deque()
        )

        app.mount('ThreadsList', _objects)

    def getById(self, id: int):
        for item in self.items:
            if item.global_id == id:
                return item

    def getAll(self) -> Generator[ExecutionThread]:
        for item in self.items:
            yield item

    def add(self, item: ExecutionThread):
        item.global_id = app.app.threads_id.getIndex()
        self.log('new thread: {0}'.format(item.global_id), role = ['thread.created', 'thread'])

        self.items.append(item)

    def remove(self, item: ExecutionThread):
        if item in self.items:
            self.items.remove(item)
