#from App.Responses.Response import Response
from App.Objects.Mixins.BaseModel import BaseModel

class Updateable():
    async def update(self, old: BaseModel, response: BaseModel) -> BaseModel:
        return response
