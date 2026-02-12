from App.Objects.Relations.Link import Link
from Media.Files.File import File
from pydantic import Field
from pathlib import Path
from App import app

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

    async def _get_virtual_linked(self, with_role = None):
        for item in self.get_content():
            item.obj.set_tmp()
            item.local_obj.make_possible_to_use_dynamic_links()
            item.local_obj.make_public()
            item.flush(app.Storage.get(self.getDbName()))
            item.save()

            yield Link(
                item = item
            )
