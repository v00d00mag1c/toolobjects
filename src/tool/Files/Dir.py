from Files.File import File
from pydantic import Field
from pathlib import Path

class Dir(File):
    is_dir: bool = Field(default = True)

    def getContent(self) -> list:
        path = Path(self.path)
        files = []

        new_item = None
        for item in path.iterdir():
            if item.is_dir():
                new_item = Dir(
                    path = str(item)
                )
            else:
                new_item = File(
                    path = str(item),
                )

        new_item.countStats()
        files.append(new_item)

        return files
