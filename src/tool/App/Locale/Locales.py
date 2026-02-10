from App.Objects.Object import Object
from App.Objects.Arguments.ListArgument import ListArgument
from App.Objects.Arguments.Argument import Argument
from App.Locale.Lang import Lang
from Data.Types.String import String
from Data.Types.JSON import JSON
from typing import Generator
from pydantic import Field
from pathlib import Path
from App import app

class Locales(Object):
    langs: list[Lang] = Field(default = [])
    has_loaded_langs: bool = Field(default = False)

    def getItems(self) -> Generator[Lang]:
        for item in self.langs:
            yield item

    def get(self, key: str, *args) -> str:
        if self.has_loaded_langs == False:
            self._load_langs()

        _lang = None
        _current = self.getOption('app.locales.current')
        for item in self.langs:
            if _current == item.id:
                _lang = item
                break

        if _lang != None:
            _key = _lang.get(key)
            if _key == None:
                return '@' + key

            return _key.get_value(args)
        else:
            self.log_error(f'lang is not set (current {0})'.format(_current))
            return key

    @classmethod
    def mount(cls):
        locales = cls()
        app.mount('Locales', locales)

    def _load_langs(self):
        for lang in list(self.get_default_langs()) + self.getOption('app.locales.langs'):
            try:
                _lang = self._load_lang_by_path(lang)
                self.langs.append(_lang)
                self.log_success('loaded lang {0} with id {1}'.format(lang, _lang.id), role = ['lang.loaded'])
            except Exception as e:
                self.log_error(e, exception_prefix='error loading lang {0}:'.format(lang))

        self.has_loaded_langs = True

    def get_default_langs(self):
        for item in app.app.src.joinpath('locales').iterdir():
            if item.suffix == '.json':
                yield item

    def _reset_langs(self):
        self.has_loaded_langs = False
        self.langs = []

    @classmethod
    def _load_lang_by_path(cls, path: str) -> Lang:
        _path = Path(path)
        _text = _path.read_text(encoding='utf-8')
        _json = JSON.fromText(_text)

        return Lang(**_json.data)

    @classmethod
    def _settings(cls):
        return [
            ListArgument(
                name = 'app.locales.langs',
                default = [],
                orig = String,
            ),
            Argument(
                name = 'app.locales.current',
                default = 'en_US',
                orig = String,
            )
        ]
