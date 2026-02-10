from App.Server import Server
from App.Objects.Requirements.Requirement import Requirement
from Data.Types.JSON import JSON
from App.ACL.Tokens.Get import Get as TokensGet
from App import app
import aiohttp
import aiohttp_jinja2
import jinja2

from App.Client.Pages.App.Index import Index as PageIndex

class Client(Server):
    displayments: dict = {}

    def _before_run(self, i):
        _templates = str(app.app.src.joinpath('tool').joinpath('App').joinpath('Client').joinpath('Pages'))
        aiohttp_jinja2.setup(self._app, 
                             loader=jinja2.FileSystemLoader(_templates),
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

        return {
            'app_name': self.getOption('app.name'),
            'user': self._get_current_user(request),
            'tr': app.Locales.get,
            'request': request,
            'current_url': request.rel_url,
            'global_app_categories': categories,
            'len': len
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
                    'username': data.get('username', '').strip(),
                    'password': data.get('password', '').strip(),
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
            if self.displayments.get(module.for_object) == None:
                self.displayments[module.for_object] = []

            self.displayments[module.for_object].append(module)

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
            return await item.render_as_page(request, _context)
        except Exception as e:
            _context.update({'error_message': str(e)})

            self.log_error(e)
            return await PageIndex().render_as_error(request, _context)
