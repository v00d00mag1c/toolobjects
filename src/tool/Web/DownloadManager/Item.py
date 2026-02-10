from App.Objects.Object import Object
from pydantic import Field
from typing import Any
import asyncio, datetime
from App.Logger.LogPrefix import LogPrefix
from Web.HTTP.RequestHeaders import RequestHeaders
from pathlib import Path

class NotFoundError(Exception):
    pass

class AccessDeniedError(Exception):
    pass

class Item(Object):
    _manager_link: Any = None
    _task: Any = None
    _run_flag: Any = None #asyncio.Event
    _request: Any = None

    url: str = Field()
    name: str = Field()
    state: str = Field(default = 'started') # TODO literal
    downloaded_bytes: int = Field(default = 0)
    download_dir: str = Field()
    started_at: datetime.datetime = Field(default = None)
    response_iter: int = Field(default = 1024)
    save_to_file: bool = Field(default = True)
    _unserializable = ['_task', '_run_flag']

    def _init_hook(self):
        self._run_flag = asyncio.Event()
        self.id = self._manager_link.queue.downloads.getIndex()

    def pause(self):
        self._run_flag.clear()

    def resume(self):
        self._run_flag.set()

    def getPath(self):
        return Path(self.download_dir).joinpath(self.name)

    async def start(self, new_headers: dict = {}) -> asyncio.Task:
        async with self._manager_link.getSession() as session:
            self.log(f"URL: {self.url}")
            self.started_at = datetime.datetime.now()
            self.resume()
            self._task = await asyncio.create_task(self.download(session, new_headers))

            return self._task

    async def download(self, session, new_headers: RequestHeaders = {}):
        _headers = self._manager_link.getHeaders().to_minimal_json()
        _headers.update(new_headers.to_minimal_json())

        self.log('making call to {0} with headers {1}'.format(self.url, _headers))

        async with self._manager_link.semaphore:
            request = session.get(self.url,
                                       allow_redirects=self._manager_link.getOption('download_manager.allow_redirects'), 
                                       headers=_headers,
                                       timeout = self._manager_link.timeout)

            async with request as response:
                status = response.status
                if status == 404:
                    raise NotFoundError('404 error')

                if status == 403:
                    _read = await response.content.read()
                    self.log_error('access denied, error: {0}'.format(_read.decode("utf8")))

                    raise AccessDeniedError('access denied')

                assert status not in [404, 403], '{0} error'.format(status)

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
                await self._run_flag.wait()

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
