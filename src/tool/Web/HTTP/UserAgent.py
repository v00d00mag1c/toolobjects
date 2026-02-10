from App.Objects.Misc.Valueable import Valueable
from pydantic import Field
import ua_generator

class UserAgent(Valueable):
    @classmethod
    def get_or_generate(cls):
        _conf = cls.getOption('download_manager.headers.user-agent')
        if _conf == '':
            return cls.generate()

        return _conf

    @staticmethod
    def generate():
        return ua_generator.generate(device='desktop', browser=['chrome', 'edge']).text
