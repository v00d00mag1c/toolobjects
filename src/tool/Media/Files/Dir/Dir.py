from Media.Files.File import File
from pydantic import Field
from pathlib import Path

class Dir(File):
    is_dir: bool = Field(default = True)

    def get_content(self) -> list:
        path = Path(self.path)
        files = []

        for item in path.iterdir():
            new_item = None
            if item.is_dir():
                new_item = Dir(
                    path = str(item)
                )
            else:
                new_item = File(
                    path = str(item),
                )

            new_item._count_stats()
            files.append(new_item)

        return files
