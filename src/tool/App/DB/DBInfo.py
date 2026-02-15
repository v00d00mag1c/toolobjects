from pydantic import BaseModel

class DBInfo(BaseModel):
    uuid: str
    db_name: str
