from App.DB.Adapters.SQLAlchemy import SQLAlchemy
from App.DB.Query.Condition import Condition
from pydantic import Field

class SQLite(SQLAlchemy):
    protocol_name = 'sqlite'
    content: str = Field(default = None)
    delimiter = ':///'
    check_same_thread: bool = Field(default = True)
    echo: bool = Field(default = False)

    def _get_sqlalchemy_connection_string(self):
        _content = ''
        if self.content != None:
            _content = str(self.content) 
        else:
            _content = str(self._storage_item.get_storage_adapter().getDir().joinpath(self.name + '.db'))

        return _content

    def _get_engine(self, connection_str: str):
        from sqlalchemy import create_engine
        from sqlalchemy.pool import StaticPool

        if self.check_same_thread == False:
            self._engine = create_engine(
                connection_str,
                echo = self.echo,
                connect_args = {
                    'check_same_thread': False
                },
                poolclass = StaticPool
            )
        else:
            self._engine = create_engine(
                connection_str,
                echo = self.echo,
            )
