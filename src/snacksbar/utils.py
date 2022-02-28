import ujson
from pydantic import BaseModel


class APIModel(BaseModel):
    class Config:
        json_loads: ujson.loads
        json_dumps: ujson.dumps
        orm_mode = True
