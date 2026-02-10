from App.Objects.Arguments.ArgumentDict import ArgumentDict
from App.Objects.Arguments.Argument import Argument
from Data.Types.String import String
from Data.Types.Boolean import Boolean
from App.Objects.Index.Namespaces.Add.Add import Add
from App import app
from pathlib import Path
import zipfile
import datetime

class FromZip(Add):
    @classmethod
    def _arguments(cls) -> ArgumentDict:
        return ArgumentDict(items = [
            Argument(
                name = 'path',
                orig = String,
                default = None
            ),
            Argument(
                name = 'url',
                orig = String,
                default = None
            ),
            Argument(
                name = 'save_dir',
                default = None,
                orig = String
            ),
            Argument(
                name = 'zip_password',
                default = None,
                orig = String
            )
        ],
        missing_args_inclusion = True)

    async def _implementation(self, i):
        self.check_confirm(i.get('confirm'))

        _name = i.get('name')
        _pass = i.get('zip_password')
        _save_dir = i.get('save_dir')
        zip_path = None

        if i.get('path') != None:
            zip_path = Path(i.get('path'))
            assert zip_path.is_dir() == False, 'use FromDir instead'

            if _name == None:
                _name = zip_path.stem
        elif i.get('url') != None:
            _now = round(datetime.datetime.now().timestamp(), 0)
            _download_to = app.app.cwd.joinpath('Custom')
            _tmp_name = str(_now) + '.zip'
            if _name == None:
                _name = str(_now)

            zip_path = _download_to.joinpath(_tmp_name)

            item = app.DownloadManager.addURL(i.get('url'), _download_to, _tmp_name)
            await item.start()
        else:
            raise Exception('nothing passed')

        if _save_dir == None:
            _save_dir = app.app.cwd.joinpath('Custom')
            _save_dir = _save_dir.joinpath(_name)
            _save_dir.mkdir(exist_ok = False)

        with zipfile.ZipFile(str(zip_path), "r") as zip_ref:
            if _pass == None:
                zip_ref.extractall(_save_dir)
            else:
                zip_ref.extractall(_save_dir, pwd = _pass)

        if i.get('url') != None:
            zip_path.unlink()

        i.set('add_path', str(_save_dir) + '\\objects')
        i.set('name', _name)

        self._install(i)
