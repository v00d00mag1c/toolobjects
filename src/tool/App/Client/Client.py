from App.Server import Server
from App.Objects.Requirements.Requirement import Requirement
from Data.Types.JSON import JSON
from Data.Types.String import String
from App.ACL.Tokens.Get import Get as TokensGet
from App import app
import aiohttp
import aiohttp_jinja2
import jinja2
from urllib.parse import quote

from App.Client.Pages.App.Index import Index as PageIndex
from App.Objects.Arguments.Argument import Argument
from App.Objects.Arguments.ListArgument import ListArgument
from App.Storage.StorageUUID import StorageUUID
from Data.Primitives.Collections.Collection import Collection
from Data.Types.Boolean import Boolean
from Data.Types.Dict import Dict
from Web.Bookmarks.Bookmark import Bookmark
from pathlib import Path

class Client(Server):
    displayments: dict = {}

    def _before_run(self, i):
        pathes = list()
        namespaces = app.ObjectsList.namespaces
        for item in namespaces:
            if item.has_root():
                pathes.append(Path(item.root).joinpath('App').joinpath('Client').joinpath('Pages'))

        aiohttp_jinja2.setup(self._app, 
                             loader=jinja2.FileSystemLoader(pathes),
                             auto_reload = True)

    @classmethod
    def _requirements(cls) -> list:
        return [
            Requirement(
                name = 'Jinja2'
            ),
            Requirement(
                name = 'aiohttp-jinja2'
            )
        ]

    def _get_tokens(self, request):
        users = list()

        try:
            _json = JSON.fromText(request.cookies.get('tokens'))
            users = _json.data
        except Exception as e:
            self.log_error(e)

        return users

    def _get_bookmarks_collection(self, user):
        option_id = 'web.bookmarks.collection_id'
        collection_id = self.getOption(option_id)
        if collection_id == None:
            collection_id = {}

        collection = None

        if collection_id.get(user.name) == None:
            common = app.Storage.get('common')
            collection = Collection()
            collection.flush(common)
            collection.save()
            collection_id[user.name] = collection.getDbIds()

            app.Config.getItem().set(option_id, collection_id)
        else:
            collection = StorageUUID.fromString(collection_id.get(user.name)).toPython()

        return collection

    def _check_bookmarks(self, collection):
        try:
            for link in collection.getLinked():
                if link.item.isInstance(Bookmark):
                    yield link.item
        except Exception as e:
            self.log_error(e, exception_prefix="Error getting bookmarks: ")

    def _get_template_context(self, request):
        categories = {
            'client.index.content': [],
            'client.app': [],
        }

        for key, val in app.app.view.displayments.items():
            menu = val[0].get_menu()
            if menu != None:
                if categories.get(menu.category_name) is None:
                    categories[menu.category_name] = []

                categories[menu.category_name].append(menu)

        current_user = self._get_current_user(request)
        bookmarks_collection = self._get_bookmarks_collection(current_user)

        return {
            'app_name': self.getOption('app.name'),
            'user': current_user,
            '_': app.Locales.get,
            'request': request,
            'global_app_categories': categories,
            'len': len,
            'String': String,
            'url_for_object': '?i=App.Objects.Object&uuids=',
            'current_url': request.rel_url,
            'current_url_encoded': quote(str(request.rel_url)),
            'ref': request.rel_url.query.get('ref'),
            'theme': request.cookies.get('theme'),
            '_app_bookmarks_collection': bookmarks_collection,
            '_app_bookmarks': list(self._check_bookmarks(bookmarks_collection))
        }

    def _auth(self, args: dict, request):
        if args.get('auth') == None:
            args['auth'] = self._get_current_user(request)
        else:
            args['auth'] = self._auth_middleware(args.get('auth'))

        if args.get('auth') != None:
            # self.log('auth as {0}'.format(args.get('auth').name))

            return args.get('auth')
        else:
            pass

    def _get_current_user(self, request):
        for item in self._get_tokens(request):
            if item.get('is_common'):
                return self._auth_middleware(item.get('token'))

    def check_login(func):
        async def _check(*args, **kwargs):
            user = args[0]._get_current_user(args[1])
            if user == None:
                raise aiohttp.web.HTTPFound('/login')

            return await func(*args)

        return _check

    def _getCustomRoutes(self):
        return [
            ('/login', self._login, ('get', 'post')),
            ('/logout', self._logout, ['get']),
        ]

    async def _login(self, request):
        if request.method == 'GET':
            return aiohttp_jinja2.render_template('Users/login.html', request, {})
        else:
            try:
                response = aiohttp.web.HTTPFound('/')
                data = await request.post()
                token = await TokensGet().execute({
                    'username': data.get('_escapysm_username', '').strip(),
                    'password': data.get('_escapysm_password', '').strip(),
                    'infinite': True
                })
                _tokens = self._get_tokens(request)
                _tokens.append({
                    'token': token.items[0].value,
                    'is_common': True
                })

                response.set_cookie('tokens', JSON(data = _tokens).dump())

                return response
            except Exception as e:
                return aiohttp_jinja2.render_template('Users/login.html', request, {'special_message': str(e)})

    async def _logout(self, request):
        response = aiohttp.web.HTTPFound('/')
        _tokens = self._get_tokens(request)
        for item in _tokens:
            item['is_common'] = False

        if request.rel_url.query.get('clear') == '1':
            _tokens = []

        response.set_cookie('tokens', JSON(data = _tokens).dump())

        return response

    def init_hook(self):
        for item in app.ObjectsList.getObjectsByCategory(['App', 'Client', 'Pages']):
            module = item.getModule()
            for_object = module.for_object
            if type(for_object) == str:
                for_object = [for_object]

            for for_item in for_object:
                if self.displayments.get(for_item) == None:
                    self.displayments[for_item] = []

                self.displayments[for_item].append(module)

    @check_login
    async def _index(self, request):
        _context = self._get_template_context(request)
        query = request.rel_url.query
        object_name = query.get('i', 'App.Client.Client')
        displayment = self.displayments.get(object_name)

        self.log('request to displayment {0}'.format(object_name), role = ['displayment_client_request'])

        if displayment == None or len(displayment) == 0:
            _context.update({'error_message': 'Not found displayment for {0}'.format(object_name)})

            return await PageIndex().render_as_error(request, _context)

        try:
            item = displayment[0]()
            item.request = request
            item.context = _context
            item.auth = self._get_current_user(request)
            return await item.render_as_page()
        except Exception as e:
            _context.update({'error_message': str(e)})

            self.log_error(e)
            return await PageIndex().render_as_error(request, _context)

    @classmethod
    def _settings(cls) -> list:
        return [
            Argument(
                name = 'web.bookmarks.collection_id',
                default = None,
                orig = Dict
            ),
            ListArgument(
                name = 'web.index.collection',
                default = None,
                orig = StorageUUID
            )
        ]
