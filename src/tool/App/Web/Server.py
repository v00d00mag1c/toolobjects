from App.Objects.View import View
from App.Objects.Object import Object
from App.Objects.Arguments.Argument import Argument
from App.Objects.Responses.Error import Error
from Data.String import String
from Data.Int import Int
from Data.Boolean import Boolean
from Data.JSON import JSON
from aiohttp import web
from App import app
from pathlib import Path
from App.DB.Adapters.Search.Condition import Condition
from App.Storage.StorageUnit import StorageUnit
import asyncio, traceback

class Server(View):
    async def implementation(self, i):
        _pre_i = i.get('pre_i')

        _assets = app.app.src.joinpath('assets')
        _client = _assets.joinpath('client')
        _host = self.getOption("web.options.host")
        _port = self.getOption("web.options.port")
        _app = web.Application()
        _ws_connections = list()

        def _spa(request):
            return web.Response(
                text =
                """
                <html>
                    <head>
                        <script defer src="/static/client/node_modules/alpinejs/dist/cdn.min.js"></script>
                    </head>
                    <body>
                        <script type="module">
                            import { App } from "/static/client/App/App.js"

                            window.app = new App()
                            await window.app.run()
                        </script>
                    </body>
                </html>
                """,
                content_type = 'text/html'
            )

        def _get_asset(request):
            asset_path  = request.match_info.get('path', '')
            static_file = _assets.joinpath(asset_path)

            _msg = f"asset request to {str(asset_path)}"
            try:
                assert static_file.exists() == True and static_file.is_file() == True
                static_file.resolve().relative_to(_assets.resolve())
            except (ValueError, RuntimeError, AssertionError):

                self.log(_msg + ", failed.")
                raise web.HTTPForbidden(reason="Not found / Access denied")

            self.log(_msg)

            return web.FileResponse(static_file)

        def _get_js_lib(request):
            asset_path  = request.match_info.get('path', '')
            static_file = app.app.src.joinpath(asset_path)
            try:
                assert static_file.exists() == True and static_file.is_file() == True
                assert static_file.suffix == '.js'
                static_file.resolve().relative_to(app.app.src.resolve())
            except (ValueError, RuntimeError, AssertionError):
                raise web.HTTPForbidden(reason="Not found / Access denied")

            return web.FileResponse(static_file)

        def _get_storage_unit(request):
            uuid = int(request.match_info.get('uuid', ''))
            _storage = request.match_info.get('storage', '')
            path = request.match_info.get('path', '')

            storage = app.Storage.get(_storage)

            _query = storage.adapter.getQuery()
            _query.addCondition(Condition(
                val1 = 'uuid',
                operator = '==',
                val2 = uuid
            ))

            storage_unit = _query.first()
            if storage_unit == None:
                return web.HTTPNotFound(text="Not found storage_unit")

            storage_unit = storage_unit.toPython()
            if storage_unit.isInstance(StorageUnit) == False:
                return web.HTTPNotFound(text="Item is not a storage unit")

            storage_path = storage_unit.getDir()
            file = storage_path / path

            try:
                file.resolve().relative_to(storage_path.resolve())
            except (ValueError, RuntimeError):
                raise web.HTTPForbidden(reason="Access denied")

            if not file.is_file():
                raise web.HTTPNotFound(text="Not found file")

            return web.FileResponse(str(file))

        async def _call_shortcut(pre_i, args):
            _json = JSON(data = {})
            results = None
            args['auth'] = app.AuthLayer.login(
                name = args.get('username'),
                password = args.get('password'),
                login_from = 'web'
            )

            try:
                results = await pre_i.execute(args)
            except Exception as e:
                results = Error(
                    name = e.__class__.__name__,
                    message = str(e)
                )
                traceback.print_exception(e)

            _json.data = results.to_json()

            return _json

        async def _single_call(request):
            pre_i = _pre_i()
            #i = request.match_info.__dict__()
            _i = await request.json()
            self.log('Calling, i={0}'.format(_i.get('i')))

            _json = _call_shortcut(pre_i, _i)

            return web.Response(
                text = _json.dump(),
                content_type = 'application/json'
            )

        async def _ws(request):
            ws = web.WebSocketResponse()
            await ws.prepare(request)
            self.log('websocket connection')

            _ws_connections.append(ws)

            async for msg in ws:
                try:
                    if msg.type != web.WSMsgType.TEXT:
                        continue

                    data = JSON.fromText(text = msg.data).data
                    _type = data.get('type')
                    _event_index = int(data.get('event_index'))
                    _payload = data.get('payload')

                    self.log('got message {0}, index {1}'.format(_type, _event_index))

                    if _type == 'object':
                        pre_i = _pre_i()
                        pre_i.set_event_index(_event_index)
                        results = await _call_shortcut(pre_i, _payload)

                        await ws.send_str(JSON(data={
                            'type': _type,
                            'event_index': _event_index,
                            'payload': results.data
                        }).dump())
                except Exception as e:
                    traceback.print_exception(e)

            _ws_connections.remove(ws)

            return ws

        async def _upload_storage_unit(request):
            _storage = request.match_info.get('storage', '')
            storage = app.Storage.get(_storage)
            if storage == None:
                raise web.HTTPNotAcceptable(text="not found storage")

            data = await request.post()
            file = data.get('file')
            if file == None:
                raise web.HTTPNotAcceptable(text="not passed file")

            storage_unit = storage.getStorageUnit()
            filename = storage_unit.hash + '.oct'
            file_path = storage_unit.getDir().joinpath(filename)

            with open(file_path, 'wb') as f:
                f.write(file.file.read())

            storage_unit.save()

            return web.Response(
                text = JSON(data = storage_unit.to_json()).dump(),
                content_type = 'application/json'
            )

        for route in [
            ('/', _spa, 'get'),
            ('/static/{path:.*}', _get_asset, 'get'),
            ('/storage/{storage}/{uuid}/{path:.*}', _get_storage_unit, 'get'),
            ('/storage/js/', _get_js_lib, 'post'),
            ('/api', _single_call, 'get'),
            ('/rpc', _ws, 'get'),
            ('/api/upload/{storage}', _upload_storage_unit, 'post'),
        ]:
            getattr(_app.router, 'add_' + route[2])(route[0], route[1])#(route[0], getattr(self, route[1]))

        runner = web.AppRunner(_app)
        await runner.setup()

        async def _log_ws(to_print, check_categories):
            for connection in _ws_connections:
                await connection.send_str(JSON(data={
                    'type': 'log',
                    'event_index': 0,
                    'payload': to_print.to_json()
                }).dump())
        
        app.Logger.addHook('log', _log_ws)

        site = web.TCPSite(
            runner,
            host = _host,
            port = _port
        )

        await site.start()

        _http = 'http://'
        self.log("Started server on {0}{1}:{2}".format(_http, _host, _port))

        while True:
            await asyncio.sleep(3600)

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
                default = '22222',
                orig = Int
            ),
            Argument(
                name = 'web.aiohttp.debug',
                default = True,
                orig = Boolean
            ),
            Argument(
                name = 'app.name',
                default = 'toolobjects',
                orig = String
            )
        ]
