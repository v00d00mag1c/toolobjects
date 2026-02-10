from App.Objects.Act import Act
from App import app

class Reload(Act):
    def _implementation(self, i):
        app.Locales._reset_langs()
        app.Locales._load_langs()
