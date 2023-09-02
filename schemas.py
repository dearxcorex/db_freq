from pydantic import BaseModel
import models

class freqBase(BaseModel):
    freq:float
    institution:str
    usage: str

class freqResponse(freqBase):
    freq:float
    institution:str
    usage: str

    class Config():
        from_attributes = True


class freqUpdateResponse(BaseModel):
    freq:float 
    institution:str 
    usage: str

    class Config():
        from_attributes = True