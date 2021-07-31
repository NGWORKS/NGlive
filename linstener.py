"""
监听器

>> 用于监听各种事件并响应
>> 是本项目 生产者-消费者模型中重要的一环

"""
from db import RecorderDB,Rate
import uuid,os,datetime
from pathlib import Path
from orm import RateOrm
from initial import works_path,out_path,first_factory,second_factory
from log import logger
import json,os,time

class RecorderListener:
    """
    录播姬事件监听器
    --------------

    用于监听-响应录播姬的三种事件：

    * SessionStarted 直播开启
    * FileOpening 文件打开
    * FileClosed 文件关闭
    * SessionEnded 直播关闭
    """
    def __init__(self,ws) -> None:
        self.ws = ws

    def send(self,message):
        try:
            self.ws.send(json.dumps(message))
        except:
            logger.warning('ws推送失败，请检查网络连接')

    def SessionStarted(self,event):
        # 开播/手动开始
        data = event.dict["artical"]
        logger.info(f"直播间{data.EventData.RoomId}开播/手动开始录制")
        self.send({'CMD':"SessionStarted",'ID':data.EventData.SessionId})

    def FileOpening(self,event):
        # 文件打开
        data = event.dict["artical"]
        logger.info(f"直播间{data.EventData.RoomId}新录制文件打开")
        # 生成唯一的task id
        taskid = str(uuid.uuid1())
        time_now = time.strftime("%Y%m%d", time.localtime())
        # 用于新建相应的输出目录
        output = str(Path('/') / out_path / str(time_now) / str(data.EventData.RoomId) )
        if not os.path.isdir(output):
            os.makedirs(output)

        # 当文件打开时 向 流程数据表添加一个新纪录
        with RecorderDB(Rate) as f:
            f.add(
                TaskId = taskid,
                SessionId = data.EventData.SessionId,
                RoomId = data.EventData.RoomId,
                File = Path(data.EventData.RelativePath).name,
                StartTime = data.EventData.FileOpenTime, 
                Origin = str(Path('/') / works_path / data.EventData.RelativePath),
                OutPut = str(Path('/') / output / f'{Path(data.EventData.RelativePath).stem}.mp4'),
                Recorder = False
            )
            self.send({'CMD':"FileOpening",'ID':taskid})

    def FileClosed(self,event):
        # 文件关闭
        data = event.dict["artical"]
        logger.info(f"直播间{data.EventData.RoomId}一个文件完成录制，文件关闭")
        # 更新流程数据表
        with RecorderDB(Rate) as f:
            Ratedata = f.filter(File = Path(data.EventData.RelativePath).name)[0]
            Ratedata.Recorder = True
            co_model = RateOrm.from_orm(Ratedata)
            if len(first_factory) != 0:
                for q in first_factory:
                    q.append(co_model)
            self.send({'CMD':"FileClosed",'ID':co_model.TaskId})

    def SessionEnded(self,event):
        # 关播/手动停止
        data = event.dict["artical"]
        logger.info(f"直播间{data.EventData.RoomId}关播/手动结束录制")
        self.send({'CMD':"SessionEnded",'ID':data.EventData.SessionId})


    
class TranscodeListener:
    """
    转码事件响应
    -----------

    用于监听-响应转码的四种事件：

    * TranscodeStarted 开始转码
    * IsTranscode 文件转码中
    * TranscodeEnded 转码结束（成功）
    * TranscodeError 转码错误
    """
    def __init__(self,ws) -> None:
        self.ws = ws

    def send(self,message):
        try:
            self.ws.send(json.dumps(message))
        except:
            logger.warning('ws推送失败，请检查网络连接')

    def TranscodeStarted(self,event):
        # 开始转码
        task = event.dict["artical"]
        with RecorderDB(Rate) as f:
            data = f.filter(TaskId = task.tasksid)[0]
            data.Transcode = False
        logger.info(f"任务{task.tasksid} 开始转码")
        self.send({'CMD':"TranscodeStarted",'ID':task.tasksid})
    
    def IsTranscode(self,event):
        # 正在转码
        task = event.dict["artical"]
        logger.debug(f"任务{task.tasksid} 正在转码,进度{task.progress}%")
        self.send({'CMD':"IsTranscode",'ID':task.tasksid,'COMP':task.progress})
    
    def TranscodeEnded(self,event):
        # 结束转码
        task = event.dict["artical"]
        with RecorderDB(Rate) as f:
            data = f.filter(TaskId = task.tasksid)[0]
            data.Transcode = True
            co_model = RateOrm.from_orm(data)
            if len(second_factory) != 0:
                for q in second_factory:
                    if q[0] == "After_Transcode":
                        q[1].append(co_model)
        logger.info(f"任务{task.tasksid} 结束转码")
        self.send({'CMD':"TranscodeEnded",'ID':task.tasksid})
    
    def TranscodeError(self,event):
        # 转码出错
        task = event.dict["artical"]
        with RecorderDB(Rate) as f:
            data = f.filter(TaskId = task.tasksid)[0]
            data.Error = True       
            data.EndedTime = datetime.datetime.now()
        logger.error(f"任务{task.tasksid} 转码出错")
        self.send({'CMD':"TranscodeError",'ID':task.tasksid})

class UpListener:
    """
    上传事件响应
    -----------

    用于监听-响应转码的四种事件：

    * UpStarted 开始上传
    * IsUp 上传中
    * UpEnded 上传结束（成功）
    * UpError 上传错误
    """
    def __init__(self,ws) -> None:
        self.ws = ws

    def send(self,message):
        try:
            self.ws.send(json.dumps(message))
        except:
            logger.warning('ws推送失败，请检查网络连接')
    def UpStarted(self,event):
        # 开始上传
        task = event.dict["artical"]
        with RecorderDB(Rate) as f:
            data = f.filter(TaskId = task.tasksid)[0]
            data.Upload = False
        logger.info(f"任务{task.tasksid} 开始上传")
        self.send({'CMD':"UpStarted",'ID':task.tasksid})
        
    
    def IsUp(self,event):
        # 正在上传
        task = event.dict["artical"]
        logger.debug(f"任务{task.tasksid} 正在上传,进度{task.progress}%")
        self.send({'CMD':"IsUp",'ID':task.tasksid,'COMP':task.progress})
    
    def UpEnded(self,event):
        # 结束上传
        task = event.dict["artical"]
        with RecorderDB(Rate) as f:
            data = f.filter(TaskId = task.tasksid)[0]
            data.Upload = True       
            data.EndedTime = datetime.datetime.now()
            co_model = RateOrm.from_orm(data)
            if len(second_factory) != 0:
                for q in second_factory:
                    if q[0] == "After_Up":
                        q[1].append(co_model)
        logger.info(f"任务{task.tasksid} 结束上传")
        self.send({'CMD':"UpEnded",'ID':task.tasksid})
    
    def UpError(self,event):
        # 上传出错
        task = event.dict["artical"]
        with RecorderDB(Rate) as f:
            data = f.filter(TaskId = task.tasksid)[0]
            data.Error = True       
            data.EndedTime = datetime.datetime.now()
        logger.error(f"任务{task.tasksid} 上传出错")
        self.send({'CMD':"UpError",'ID':task.tasksid})


