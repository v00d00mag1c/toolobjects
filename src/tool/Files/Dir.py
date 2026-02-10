from Files.File import File
from pydantic import Field
from pathlib import Path

class Dir(File):
    is_dir: bool = Field(default = True)

    def getContent(self) -> list:
        from Files.File import File

        path = Path(self.path)
        files = []

        for item in path.iterdir():
            if item.is_dir():
                files.append(Dir(
                    path = str(item)
                ))
            else:
                files.append(File(
                    path = str(item),
                ))

        return files
