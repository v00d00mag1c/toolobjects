from App.Objects.Object import Object
from App.Objects.Arguments.ListArgument import ListArgument
from App.Objects.Arguments.Argument import Argument
from App.Locale.Lang import Lang
from Data.String import String
from Data.JSON import JSON
from typing import Generator
from pydantic import Field
from pathlib import Path
from App import app

class Locales(Object):
    langs: list[Lang] = Field(default = [])

    def getItems(self) -> Generator[Lang]:
        for item in self.langs:
            yield item

    def get(self, key: str) -> str:
        _lang = None
        _current = self.getOption('app.locales.current')
        for item in self.langs:
            if _current == item.id:
                _lang = item
                break

        if _lang != None:
            return _lang.get(key)

    @classmethod
    def mount(cls):
        locales = cls()

        for lang in cls.getOption('app.locales.langs'):
            try:
                locales.langs.append(locales._load_lang_by_path(lang))
                locales.log_success('loaded lang {0}'.format(lang))
            except Exception as e:
                locales.log_error(e, exception_prefix='error loading lang {0}'.format(lang))

        app.mount('Locales', locales)

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
                default = None,
                orig = String,
            )
        ]
