from App.DB.Adapters.MySQL import MySQL
from App.Objects.Requirements.Requirement import Requirement
from App.DB.Query.Condition import Condition

class PostgreSQL(MySQL):
    protocol_name = 'postgresql+pg8000'

    class QueryAdapter(MySQL.QueryAdapter):
        def _json_value(self, value):
            from sqlalchemy import func

            _fields = '.'.join(value.json_fields)
            return func.jsonb_extract_path_text(
                getattr(self._model, value.column), 
                *_fields
            )

    @classmethod
    def _requirements(cls):
        return [
            Requirement(
                name = 'pg8000'
            )
        ]

    def _get_content_column(self):
        from sqlalchemy import Column, Text
        from sqlalchemy.dialects.postgresql import JSONB

        return Column(JSONB(), nullable=False)
