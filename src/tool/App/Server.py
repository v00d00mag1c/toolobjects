from App.Objects.View import View
from App.Objects.Object import Object
from App.Objects.Arguments.Argument import Argument
from App.Objects.Arguments.ArgumentDict import ArgumentDict
from App.Objects.Responses.Error import Error

from Data.Types.String import String
from Data.Types.Int import Int
from Data.Types.Boolean import Boolean
from Data.Types.JSON import JSON
import random

from pydantic import Field
from typing import Any

from App.DB.Query.Condition import Condition
from App.DB.Query.Values.Value import Value
from App.Storage.StorageUnit import StorageUnit

import asyncio, traceback
import socket
from App.Objects.Threads.ExecutionThread import ExecutionThread

from typing import Optional, Coroutine, ClassVar
from aiohttp import web
from App import app
from pathlib import Path
import urllib
import base64

class Server(View):
    roles: ClassVar[dict] = {
        'asset_request': ['asset_request']
    }
    ws_connections: list = Field(default = list())
    pre_i: Object = Field(default = None)
    _app: Any = None
    _pre_i: Any = None
    _host: str = None

    protect_storage_units: ClassVar[bool] = True

    @classmethod
    def _settings(cls) -> list:
        return [
            Argument(
                name = 'web.options.host',
                default = '127.0.0.1',
                orig = String
            ),
            Argument(
                name = 'web.options.port',
                default = None,
                orig = Int
            ),
            Argument(
                name = 'web.aiohttp.debug',
                default = True,
                orig = Boolean
            ),
            Argument(
                name = 'app.name',
                default = 'escapysm',
                orig = String
            ),
            Argument(
                name = 'web.aiohttp.client_max_size',
                default = 10000,
                orig = Int
            )
        ]

    @classmethod
    def _arguments(cls) -> ArgumentDict:
        return ArgumentDict(items = [
            Argument(
                name = 'ignore_autostart',
                orig = Boolean,
                default = False,
            ),
            Argument(
                name = 'port',
                orig = String,
                default = None,
                config_fallback = ('web.options.port', False)
            ),
            Argument(
                name = 'host',
                orig = String,
                default = None,
                config_fallback = ('web.options.host', False)
            )
        ])

    async def _implementation(self, i):
        _host = i.get('host')
        _port = i.get('port')
        if _port == None:
            self.log('port is not passed anywhere, so it will be chosen randomly')
            _port = self._get_random_port()

        self._app = web.Application(
            client_max_size = int(self.getOption('web.aiohttp.client_max_size') ** 2)
        )
        self._pre_i = i.get('pre_i')

        self._register_default_routes(i)
        self._register_routes(i)
        self._before_run(i)

        runner = web.AppRunner(self._app)
        await runner.setup()

        self._register_ws()

        site = web.TCPSite(
            runner,
            host = _host,
            port = _port
        )

        await site.start()
        _http = 'http://'
        self._host = '{0}{1}:{2}'.format(_http, self._get_ip(_host), _port)

        if i.get('ignore_autostart') == False:
            asyncio.create_task(app.Autostart.start_them(i.get('pre_i')))

        self.log("Started server on {0}".format(self._host))

        while True:
            await asyncio.sleep(3600)

    def _before_run(self, i):
        pass

    def _get_random_port(self):
        return random.randint(1024, 49151)

    def _get_ip(self, host: str):
        if host in ['127.0.0.1', 'localhost']:
            return '127.0.0.1'

        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        ip = None
        try:
            s.connect(('8.8.8.8', 80))
            ip = s.getsockname()[0]
        except Exception:
            ip = '127.0.0.1'
        finally:
            s.close()

        return ip

    def _getCustomRoutes(self):
        return []

    def _register_routes(self, i):
        for route in self._getCustomRoutes():
            self._register_route(route)

    def _register_ws(self):
        async def _log_ws(to_print, check_categories):
            for connection in self.ws_connections:
                await connection.send_str(JSON(data={
                    'type': 'log',
                    'event_index': 0,
                    'payload': to_print.to_json()
                }).dump())

        app.Logger.addHook('log', _log_ws)

    def _register_default_routes(self, i):
        for route in [
            ('/', self._index, ['get', 'post']),
            ('/static/{path:.*}', self._get_asset, 'get'),
            ('/storage/{storage}/{uuid}/{path:.*}', self._get_storage_unit, 'get'),
            ('/api', self._single_call, ['get', 'post', 'options']),
            ('/rpc', self._ws, 'get'),
            ('/api/upload', self._upload_storage_unit, 'post'),
        ]:
            self._register_route(route)

    def _register_route(self, route: list):
        add_types = route[2]
        if type(add_types) == str:
            add_types = [add_types]

        for add_type in add_types:
            getattr(self._app.router, 'add_' + add_type)(route[0], route[1])

    def _index(self, request):
        return web.Response(
            text =
            """
            <html>
                <body></body>
            </html>
            """,
            content_type = 'text/html'
        )

    def _get_asset(self, request):
        _user = self._auth(dict(request.rel_url.query), request)
        if _user == None:
            raise web.HTTPForbidden(reason="access denied")

        _assets = app.app.src.joinpath('assets')
        asset_path  = request.match_info.get('path', '')
        static_file = _assets.joinpath(asset_path)

        _msg = f"asset request to {str(asset_path)}"
        try:
            assert static_file.exists() == True and static_file.is_file() == True
            static_file.resolve().relative_to(_assets.resolve())
        except (ValueError, RuntimeError, AssertionError):
            self.log(_msg + ", failed.", role = self.roles.get('asset_request'))
            raise web.HTTPNotFound(reason="Not found")

        self.log(_msg, role = self.roles.get('asset_request'))

        _response = web.FileResponse(static_file)
        _response.headers['Cache-Control'] = 'max-age=0'

        return _response

    def _get_storage_unit(self, request):
        if self.protect_storage_units == True:
            _user = self._auth(dict(request.rel_url.query), request)
            if _user == None:
                raise web.HTTPForbidden(reason="access denied")

        uuid = int(request.match_info.get('uuid', ''))
        _storage = request.match_info.get('storage', '')
        path = request.match_info.get('path', '')
        path = urllib.parse.unquote(path)
        decode_path = request.query.get('d') == '1'
        if decode_path:
            path = base64.urlsafe_b64decode(path.encode('utf-8')).decode()

        storage = app.Storage.get(_storage)

        _query = storage.get_db_adapter().getQuery()
        _query.addCondition(Condition(
            val1 = Value(
                column = 'uuid'
            ),
            operator = '==',
            val2 = Value(
                value = uuid
            )
        ))

        storage_unit = _query.first()
        if storage_unit == None:
            return web.HTTPNotFound(text="Not found storage_unit")

        storage_unit = storage_unit.toPython()
        if storage_unit.isInstance(StorageUnit) == False:
            return web.HTTPNotFound(text="Item is not a storage unit")

        storage_path = storage_unit.getDir()
        file: Path = storage_path.joinpath(path)

        try:
            file.absolute().relative_to(storage_path.resolve())
        except (ValueError, RuntimeError) as e:
            self.log_error(e)
            raise web.HTTPForbidden(reason="Access denied")

        if not file.is_file():
            raise web.HTTPNotFound(text="Not found file")

        return web.FileResponse(str(file))

    def _auth(self, args: dict, request = None):
        args['auth'] = self._auth_middleware(args.get('auth'))

        if args.get('auth') != None:
            self.log('auth as {0}'.format(args.get('auth').name))

            return args.get('auth')
        else:
            pass

    def _auth_middleware(self, token: str):
        return app.AuthLayer.byToken(token)

    async def _call_shortcut(self, pre_i, args: dict, event_index: int, on_event: Optional[Coroutine] = None):
        _json = JSON(data = {})
        results = None

        try:
            pre_i.add_variables_hook(on_event)

            thread = ExecutionThread(id = event_index)
            thread.set(pre_i.execute(args))
            thread.set_name(str(args.get('i')))
            results = await thread.get()
            thread.end()
        except Exception as e:
            results = Error(
                name = e.__class__.__name__,
                message = str(e)
            )
            traceback.print_exception(e)

        _json.data = results.to_json()

        return _json

    async def _single_call(self, request):
        headers = {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
            'Access-Control-Allow-Headers': 'Content-Type',
            'Access-Control-Max-Age': '86400'
        }
        if request.method == 'OPTIONS':
            return web.Response(
                text = None,
                content_type = 'application/json',
                headers = headers
            )

        pre_i = self._pre_i()
        _i = dict()
        #i = request.match_info.__dict__()
        if request.method == 'POST':
            _i = await request.post()
        else:
            _i = await request.json()

        _i = dict(_i)

        self.log('Single call, i={0}'.format(_i.get('i')))
        self._auth(_i, request)

        _json = await self._call_shortcut(pre_i, _i, -4)

        return web.Response(
            text = _json.dump(),
            content_type = 'application/json',
            headers = headers
        )

    async def _ws(self, request):
        ws = web.WebSocketResponse()
        await ws.prepare(request)
        self.log('WebSocket connection created')

        self.ws_connections.append(ws)

        async for msg in ws:
            try:
                if msg.type != web.WSMsgType.TEXT:
                    continue

                data = JSON.fromText(text = msg.data).data
                if data.get('type') == 'object':
                    asyncio.create_task(self._handle_object_mesasge(ws, self._pre_i, data))
            except Exception as e:
                traceback.print_exception(e)

        self.ws_connections.remove(ws)

        return ws

    async def _handle_object_mesasge(self, ws, pre_i, data):
        _event_type = data.get('type')
        _event_index = int(data.get('event_index'))
        _payload = data.get('payload')

        self.log('got message {0}, index {1}'.format(_event_type, _event_index))

        async def _handle_variable_message(variable):
            await ws.send_str(JSON(data={
                'type': 'variable',
                'event_index': _event_index,
                'payload': variable.serialize_self()
            }).dump())

        pre_i = pre_i()
        self._auth(_payload, None)
        results = await self._call_shortcut(pre_i, _payload, _event_index, _handle_variable_message)

        await ws.send_str(JSON(data={
            'type': _event_type,
            'event_index': _event_index,
            'payload': results.data
        }).dump())

    async def _upload_storage_unit(self, request):
        _query = request.rel_url.query
        _just_url = _query.get('return_url')
        _old_auth = _query.get('auth')
        _save_name = _query.get('save_name')
        _i_after = _query.get('i_after', None)
        _i_after_key = _query.get('i_after_key', 'storage_unit')
        _user = self._auth(dict(request.rel_url.query), request)

        if _user == None:
            raise web.HTTPForbidden(reason="access denied")

        _storage = _query.get('storage', '')
        storage = app.Storage.get(_storage)
        if storage == None:
            raise web.HTTPNotAcceptable(text="not found storage")

        data = await request.post()
        files = list()
        if data.get('file') == None:
            # Multiple files

            for field_name, value in data.items():
                if isinstance(value, web.FileField):
                    filename = value.filename
                    files.append(value)
        else:
            files.append(data.get('file'))

        if len(files) == 0:
            raise web.HTTPNotAcceptable(text="not passed file")

        storage_units = list()
        for file in files:
            _storage_unit_new = storage.get_storage_adapter().get_storage_unit()
            filename = None
            if _save_name == None:
                filename = _storage_unit_new.hash + '.oct'
            else:
                filename = _save_name

            file_path = _storage_unit_new.getDir().joinpath(filename)

            with open(file_path, 'wb') as f:
                f.write(file.file.read())

            _storage_unit_new.setCommonFile(file_path)
            _storage_unit_new.flush(storage)
            _storage_unit_new.save()

            self.log('uploaded storage unit, id {0}'.format(_storage_unit_new.getDbIds()), role = ['server.upload'])

            storage_units.append(_storage_unit_new)

        if _i_after != None:
            for storage_unit in storage_units:
                try:
                    after_action = JSON.fromText(_i_after).data
                    after_action[_i_after_key] = storage_unit
                    after_action['auth'] = _user

                    await self._pre_i().execute(after_action)
                except Exception as e:
                    self.log_error(e, exception_prefix = 'Error when uploading file: ')

        if _just_url == '1':
            return web.Response(
                text = '{0}{1}{2}?auth={3}'.format(self._host, storage_units[0].get_url(), filename, _old_auth),
                content_type = 'text/plain'
            )

        _json = JSON(data = [])
        for _item in storage_units:
            _json.data.append(_item.to_json())

        return web.Response(
            text = _json.dump(),
            content_type = 'application/json'
        )
