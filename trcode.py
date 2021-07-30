"""
转码模块

>> 对指定文件进行压制
>> 监控 ffmpeg 输出信息
>> 发送相应事件
>> TODO 可以定义参数

"""
from eventManager import Event
from taskslist import TRANSCODE
from resquest_test import TtranscodeOut
import re,math,subprocess
from log import logger

class transcode:
    """
    转码模块
    -------

    用于对指定媒体文件进行转码：

    """
    def __init__(self,eventManager):
        self.__eventManager = eventManager
        self.pros = 0

    def sendEvent(self,msg,**dt):
        """
        事件发送器
        ---------

        封装一个常用的事件发送方法

        """
        event = Event(type_=msg)
        event.dict["artical"] = TtranscodeOut(**dt)
        self.__eventManager.SendEvent(event)

    def get_seconds(self,time):
        """
        返回日志切片器
        -------------

        用于对ffmpeg 的输出日志进行相关切片操作
        """
        h = int(time[0:2])
        m = int(time[3:5])
        s = int(time[6:8])
        ms = int(time[9:12])
        ts = (h * 60 * 60) + (m * 60) + s + (ms / 1000)
        return ts

    def compute_progress_and_send_progress(self,process,tasksid):
        """
        日志解析器
        ---------

        通过正则匹配进行日志解析，获取相关数据
        """
        duration = None
        while process.poll() is None:
            line = process.stderr.readline().strip()
            if line:    
                duration_res = re.search(r'Duration: (?P<duration>\S+)', line)
                if duration_res is not None:
                    duration = duration_res.groupdict()['duration']
                    duration = re.sub(r',', '', duration)

                result = re.search(r'time=(?P<time>\S+)', line)
                
                if result is not None and duration is not None:
                    elapsed_time = result.groupdict()['time']

                    currentTime =  self.get_seconds(elapsed_time)
                    allTime = self.get_seconds(duration)

                    progress = currentTime * 100/allTime
                    progress = math.ceil(progress)
                    if progress > 100:
                        progress = 100
                    if progress != self.pros:
                        self.sendEvent("IsTranscode",tasksid = tasksid,progress = progress)
                    self.pros = progress
                    # print(f"当前压制进度：{progress}%")

    def do_ffmpeg_transcode(self,cmd,tasksid):
        """
        ffmpeg 核心
        ----------

        用于驱动FFmpeg 同时触发部分事件

        """
        try:
            process=subprocess.Popen(cmd,stderr=subprocess.PIPE,bufsize=0,universal_newlines=True,shell=True,encoding="ISO-8859-1")
            self.compute_progress_and_send_progress(process,tasksid)
            if process.returncode == 0:
                self.sendEvent("TranscodeEnded",tasksid = tasksid)
                return "success" ,process
            else:
                self.sendEvent("TranscodeError",tasksid = tasksid)
                return "error" ,process
        except:
            self.sendEvent("TranscodeError",tasksid = tasksid)




    def transcode_manege(self):
        """
        转码管理模块
        -----------

        管理转码，从任务队列中获取任务
        进行基本数据解析

        """
        logger.debug("正在初始化转码模块")
        while True:
            task = TRANSCODE.get(block=True)
            self.sendEvent("TranscodeStarted",tasksid = task.TaskId)
            cmd  = f"ffmpeg -y -i {task.Origin} -vcodec libx264 -crf 24 {task.OutPut}"
            self.do_ffmpeg_transcode(cmd,task.TaskId)

