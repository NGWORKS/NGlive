"""
使用 pydantic 整理验证各种数据
"""
from typing import Optional
from pydantic import BaseModel,validator
from datetime import datetime

class EventData(BaseModel):
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

    @validator('ShortId')
    def ShortId_is_0(cls, v):
        if v == 0:
            v = None
        return v

class Webhook(BaseModel):
    # 事件类型
    EventType : str
    # 事件id
    EventId : str
    EventData: EventData

class TtranscodeOut(BaseModel):
    # 事件类型
    tasksid : str
    # 事件id
    progress : Optional[int] = None