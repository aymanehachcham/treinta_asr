from typing import List

from pydantic import BaseModel



class CFGGeneral(BaseModel):
    pass

class CFGModel(BaseModel):
    pass

class Config(BaseModel):
    general: CFGGeneral
    models: List[CFGModel]
