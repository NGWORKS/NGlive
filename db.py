"""
此文件是用于连接和初始化数据库的程序文件。

>> 用于建立一个数据库连接
>> 新建数据库文件、新建数据表
>> 封装了一个数据库操作的类。
"""
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

# 这个是进度数据表，里面定于了每个任务唯一的ID和任务进行程度，同时记录一些必要的数据。
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

# 这个用来记录 录播姬 传来的原始数据，以供分析。
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
        # 新建连接
        self.session = DbSession()
        self.Table = Table

    def __enter__(self):
        return self

    def add(self,**dt):
        """
        这是向数据表中添加一条记录的方法
        """
        new_user = self.Table(**dt)
        # 添加到session
        self.session.add(new_user)
    
    def filter(self,**dt):
        """
        这是使用特定条件进行查询，同时使用返回的结果在关闭前可以进行数据更新。
        """
        Data = self.session.query(self.Table).filter_by(**dt).all()
        return Data

    # 在__exit__方法中捕获并输出异常信息 
    def __exit__(self, exc_type, exc_value, exc_tb):
        if exc_type:
            print(f'exc_type: {exc_type}')
            print(f'exc_value: {exc_value}')
            print(f'exc_traceback: {exc_tb}')
            print('exception handled')
            # 如果出现错误，回滚。
            self.session.rollback()
        # 提交更改
        self.session.commit()
        # 关闭连接
        self.session.close()
        return True 
