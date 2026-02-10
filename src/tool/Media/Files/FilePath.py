from Data.Types.String import String
from pathlib import Path

class FilePath(String):
    @classmethod
    def asArgument(cls, val):
        if val == None:
            return None

        return Path(val)
