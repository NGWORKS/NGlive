from taskslist import UPLOAD
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Text, Float, DateTime,Boolean
from sqlalchemy.orm import sessionmaker

# 新建连接
engine = create_engine('sqlite:///Recorder.db', encoding='utf-8', echo=False)

# 连接
DbSession = sessionmaker(bind=engine)
Base = declarative_base()

# 表信息
class Rate(Base):
    __tablename__ = "Rate"
    TaskId = Column(Text, nullable=False, primary_key=True)
    SessionId = Column(String(36), nullable=False)
    RoomId = Column(Integer, nullable=False)
    File = Column(Text,nullable=False)
    StartTime = Column(DateTime)
    EndedTime = Column(DateTime)
    Origin = Column(Text,nullable=False)
    OutPut = Column(Text)
    Clould = Column(Text)
    ShareUrl = Column(Text)
    SharePwd = Column(Text)
    Error = Column(Boolean,default=False)
    Recorder = Column(Boolean,default=None)
    Transcode = Column(Boolean,default=None)
    Upload = Column(Boolean,default=None)


class Recorder(Base):
    __tablename__ = "Recorder"
    EventId = Column(String(36), nullable=False, primary_key=True)
    SessionId = Column(String(36), nullable=False)
    EventType = Column(Text, nullable=False)
    RoomId = Column(Integer, nullable=False)
    ShortId = Column(Integer)
    Name = Column(Text, nullable=False)
    Title = Column(Text, nullable=False)
    RelativePath = Column(Text)
    FileOpenTime = Column(DateTime)
    FileCloseTime = Column(DateTime)
    FileSize = Column(Integer)
    Duration = Column(Float)

    def __init__(self, EventId, SessionId, EventType, RoomId, ShortId, Name,Title, RelativePath=None, FileOpenTime=None, FileCloseTime=None, FileSize=None, Duration=None):
        self.EventId = EventId
        self.SessionId = SessionId
        self.EventType = EventType
        self.SessionId = SessionId
        self.RoomId = RoomId
        self.ShortId = ShortId
        self.Name = Name
        self.Title = Title
        self.RelativePath = RelativePath
        self.FileOpenTime = FileOpenTime
        self.FileCloseTime = FileCloseTime
        self.FileSize = FileSize
        self.Duration = Duration


Base.metadata.create_all(engine)

class RecorderDB:
    def __init__(self,Table):
        self.session = DbSession()
        self.Table = Table

    def __enter__(self):
        return self

    def add(self,**dt):
        new_user = self.Table(**dt)
        # 添加到session
        self.session.add(new_user)
    
    def filter(self,**dt):
        Data = self.session.query(self.Table).filter_by(**dt).all()
        return Data

    # 在__exit__方法中捕获并输出异常信息 
    def __exit__(self, exc_type, exc_value, exc_tb):
        if exc_type:
            print(f'exc_type: {exc_type}')
            print(f'exc_value: {exc_value}')
            print(f'exc_traceback: {exc_tb}')
            print('exception handled')
            self.session.rollback()
        self.session.commit()
        self.session.close()
        return True # 异常处理后必须返回True


# user = session.query(QQ).filter_by(qq=10001).all()
# print(user)
