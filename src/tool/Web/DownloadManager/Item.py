from App.Objects.Object import Object
from pydantic import Field
from typing import Any
import asyncio, datetime
from App.Logger.LogPrefix import LogPrefix
from pathlib import Path

class Item(Object):
    _manager_link: Any = None
    task: Any = None
    run_flag: Any = None #asyncio.Event

    url: str = Field()
    name: str = Field()
    state: str = Field(default = 'started') # TODO literal
    downloaded_bytes: int = Field(default = 0)
    download_dir: str = Field()
    started_at: datetime.datetime = Field(default = None)
    response_iter: int = Field(default = 1024)
    save_to_file: bool = Field(default = True)

    def _constructor(self):
        self.run_flag = asyncio.Event()
        self.id = self._manager_link.queue.downloads.getIndex()

    def pause(self):
        self.run_flag.clear()

    def resume(self):
        self.run_flag.set()

    def getPath(self):
        return Path(self.download_dir).joinpath(self.name)

    async def start(self) -> asyncio.Task:
        async with self._manager_link.session as session:
            self.log(f"started download. URL: {self.url}")
            self.started_at = datetime.datetime.now()
            self.resume()
            self.task = await asyncio.create_task(self.download(session))

            return self.task

    async def download(self, session):
        async with self._manager_link.semaphore:
            self.request = session.get(self.url,
                                       allow_redirects=self._manager_link.getOption('download_manager.allow_redirects'), 
                                       headers=self._manager_link.getHeaders())

            async with self.request as response:
                status = response.status

                assert status not in [404, 403], '404'

                content_length = int(response.headers.get("Content-Length", 0))
                if content_length != None:
                    self.total_size = content_length

                    #assert self.save_to.is_file() == False, "file with this name already exists"

                await self.saveFile(response)

                self.state = "success"
                self._manager_link.triggerHooks('success', self)
                self.log_success(f"download complete")

                self.response = response

    async def saveFile(self, response) -> None:
        self.downloaded_bytes = 0

        with open(self.getPath(), 'wb') as stream:
            async for chunk in response.content.iter_chunked(self.response_iter):
                await self.run_flag.wait()

                stream.write(chunk)

                now = datetime.datetime.now()
                elapsed_time = now - self.started_at
                chunk_length = len(chunk)

                self.downloaded_bytes += chunk_length
                self._manager_link.triggerHooks("downloading", self)

                if self._manager_link.max_kbps_speed:
                    expected_time = chunk_length / (self._manager_link.max_kbps_speed)
                    if expected_time > elapsed_time:
                        await asyncio.sleep(expected_time - elapsed_time)

    @property
    def append_prefix(self) -> LogPrefix:
        return LogPrefix(name = "download_item", id = self.id)
