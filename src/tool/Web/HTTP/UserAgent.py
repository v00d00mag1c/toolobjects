from App.Objects.Misc.Valueable import Valueable
from pydantic import Field
import ua_generator

class UserAgent(Valueable):
    value: str = Field(default = None)

    @classmethod
    def get_or_generate(cls):
        _conf = cls.getOption('download_manager.user_agent')
        if _conf == None:
            return cls.generate()

        return _conf

    @staticmethod
    def generate():
        return ua_generator.generate(device='desktop', browser=['chrome', 'edge']).text
