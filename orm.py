from typing import Optional
from pydantic import BaseModel
from datetime import datetime



class Recorder(BaseModel):
    SessionId:str
    RelativePath:Optional[str] = None
    FileSize:Optional[int] = None
    FileOpenTime:Optional[datetime] = None
    FileCloseTime:Optional[datetime] = None
    Duration:Optional[float] = None
    ShortId:Optional[int] = None
    Name:str
    Title:str
    RoomId:int
    EventType : str
    EventId : str
    class Config:
        orm_mode = True

class RateOrm(BaseModel):
    TaskId:str
    SessionId:str
    File:str
    RoomId:int
    StartTime:Optional[datetime] = None
    EndedTime:Optional[datetime] = None
    Origin:str
    OutPut:Optional[str] = None
    Clould:Optional[str] = None
    ShareUrl:Optional[str] = None
    SharePwd:Optional[str] = None
    Error:Optional[bool] = False
    Recorder:Optional[bool] = None
    Transcode:Optional[bool] = None
    Upload:Optional[bool] = None

    class Config:
        orm_mode = True