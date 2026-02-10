from Media.Media import Media
from App.Objects.Requirements.Requirement import Requirement
from App.Objects.Relations.Submodule import Submodule
from Web.HTTP.RequestHeaders import RequestHeaders

class Image(Media):
    thumbnail_type = ['image']
    default_name = 'image.jpg'
    mime_type = 'image/jpeg'
    extensions = ['png', 'jpeg', 'jpg', 'gif']
    _img = None

    @classmethod
    def _submodules(cls) -> list:
        from Media.Images.Thumbnails.ResizeByPercentage import ResizeByPercentage

        return [
            Submodule(
                item = ResizeByPercentage, # You don't need a thumbnail when all files are stored locally
                role = ['thumbnail', 'thumbnail_disabled_default']
            )
        ]

    @classmethod
    def _requirements(cls):
        return [
            Requirement(
                name = 'imageio',
            )
        ]

    # or document.images
    @classmethod
    def get_page_js_function(cls):
        return '''
        document.querySelectorAll("img[src]").forEach(element => {
            elements.push(element)
        })
        document.querySelectorAll("*").forEach(element => {
            if (element.style.backgroundImage) {
                elements.push(element)
            }
        })'''

    @classmethod
    def get_page_js_insert_function(cls):
        return '''
        if (element.style.backgroundImage) {
            let _bg = element.style.backgroundImage;
            const matches = _bg.match(/url\\(['"]?([^'"()]+)['"]?\\)/);
            if (matches && matches[1]) {
                src = matches[1];
            } else {
                if (_bg.includes(',')) {
                    const urls = [];
                    const urlPattern = /url\\(['"]?([^'"()]+)['"]?\\)/g;
                    let match;
                    while ((match = urlPattern.exec(_bg)) !== null) {
                        urls.push(match[1]);
                    }
                }

                src = urls[0];
            }
        }
        '''

    def _read_file(self):
        from PIL import Image

        if self._img == None:
            _file = self.get_file()
            if _file == None:
                return None

            self._img = Image.open(str(_file.getPath()))

        return self._img

    def _reset_file(self):
        self._img = None

    def _set_dimensions(self, data):
        self.obj.width = data.size[0]
        self.obj.height = data.size[1]

    def save_hook(self):
        if self.obj.has_dimensions() == False:
            self.log('setting image dimensions...')

            try:
                _read = self._read_file()
                self._set_dimensions(_read)
            except Exception as e:
                self.log_error(e)

            self._reset_file()
