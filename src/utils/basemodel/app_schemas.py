from typing import Optional

from pydantic import BaseModel



class UUIDSchemas(BaseModel):
    uuid_token : str
    
    
class DoneTaskSchemas(BaseModel):
    uuid_token : str
    url : str
    