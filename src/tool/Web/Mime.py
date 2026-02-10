from App.Objects.Object import Object

class Mime(Object):
    @staticmethod
    def _is_binary(content_type):
        text_types = [
            'text/',
            'application/json',
            'application/xml',
            'application/javascript',
            'application/xhtml+xml',
            'application/x-www-form-urlencoded',
        ]
        binary_types = [
            'application/octet-stream',
            'application/pdf',
            'application/zip',
            'application/gzip',
            'image/',
            'audio/',
            'video/',
            'font/',
            'application/vnd.ms-',
            'application/msword',
            'application/vnd.openxmlformats-',
        ]

        if content_type.startswith('text/'):
            return False

        for text_type in text_types:
            if text_type in content_type:
                return False

        for binary_type in binary_types:
            if binary_type in content_type:
                return True

        return True

