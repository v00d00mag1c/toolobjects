from App.DB.Search.Search import Search
from Data.Search.ResultItem import ResultItem
from typing import ClassVar

class DB(Search):
    self_name: ClassVar[str] = "Search"

    def _return_objects(self, objects_list, query):
        objects_list.total_count += query.count()

        for item in query.getAll():
            try:
                obj = item.toPython()
                objects_list.append(ResultItem(
                    title = obj.any_name,
                    url = '/?i=App.Objects.Object&act=display&as={0}&redirect_if_no_displayment=on&uuids={1}'.format('self', obj.getDbIds()),
                    description = obj.any_description,
                ))
            except Exception as e:
                self.log_error(e, exception_prefix = f"{item.uuid} not printing: ")
