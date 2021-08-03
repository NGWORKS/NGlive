"""
这个程序文件实现了启动相关线程、注册监听器、自我修复的功能

>> 启动各项功能
>> 注册相应的事件监听器
>> 提供系统状态监测、各线程工作状态监测

"""
from enum import Flag
from math import fabs
from taskslist import TRANSCODE, UPLOAD
from types import resolve_bases
from upload import upload
from linstener import RecorderListener, TranscodeListener,UpListener
from threading import Thread
from eventManager import EventManager
from wsclient import *
from trcode import transcode
from up import up
import inspect
import ctypes,subprocess
from log import logger
from systemInfo import *


def _async_raise(tid, exctype):
   """raises the exception, performs cleanup if needed"""
   tid = ctypes.c_long(tid)
   if not inspect.isclass(exctype):
      exctype = type(exctype)
   res = ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, ctypes.py_object(exctype))
   if res == 0:
      raise ValueError("invalid thread id")
   elif res != 1:
      # """if it returns a number greater than one, you're in trouble,  
      # and you should call it again with exc=NULL to revert the effect"""  
      ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, None)
      raise SystemError("PyThreadState_SetAsyncExc failed")


def stop_thread(thread):
   _async_raise(thread.ident, SystemExit)

class NGlive:
    """
    NGlive初始化
    -----------
    这个类实现了启动NGlive各项功能，并且初始化事件监听器以及对于其他线程的监控。
    """
    def __init__(self) -> None:
        global transcode
        global up
        self.eventManager = EventManager()
        self.transcode = transcode(self.eventManager)
        self.up = up(self.eventManager)
        self.ws = wsc()
        self.tasksDocter__active = True
        self.up__active = True
        self.Transcode__active = True
        self.Recorder__active = True
        self.monitor__active = True
        
    def ListenerImport(self): 
        """
        初始化监听器
        -----------
        这个方法实现了初始化监听器

        * recorderlistner 用于监听-响应录播姬相关事件
        * transcodelistner 用于监听-响应转码模块相关事件
        * uplistener 用于监听-响应上传模块相关事件

        """
        logger.debug("正在初始化监听器")
        recorderlistner = RecorderListener(self.ws)
        self.eventManager.AddEventListener("SessionStarted", recorderlistner.SessionStarted)
        self.eventManager.AddEventListener("FileOpening", recorderlistner.FileOpening)
        self.eventManager.AddEventListener("FileClosed", recorderlistner.FileClosed)
        self.eventManager.AddEventListener("SessionEnded", recorderlistner.SessionEnded)
        # 压制事件监听
        transcodelistner = TranscodeListener(self.ws)
        self.eventManager.AddEventListener("TranscodeStarted", transcodelistner.TranscodeStarted)
        self.eventManager.AddEventListener("IsTranscode", transcodelistner.IsTranscode)
        self.eventManager.AddEventListener("TranscodeEnded", transcodelistner.TranscodeEnded)
        self.eventManager.AddEventListener("TranscodeError", transcodelistner.TranscodeError)
        # 上传事件监听
        uplistener = UpListener(self.ws)
        self.eventManager.AddEventListener("UpStarted", uplistener.UpStarted)
        self.eventManager.AddEventListener("IsUp", uplistener.IsUp)
        self.eventManager.AddEventListener("UpEnded", uplistener.UpEnded)
        self.eventManager.AddEventListener("UpError", uplistener.UpError)

        self.eventManager.Start()
        logger.debug("监听器初始化成功")
    
    def Recorder(self):
        logger.info("正在启动录播姬")
        Recorder__active = True
        from initial import RecorderPath,works_path,api_port
        cmd = f'"{RecorderPath}" run {works_path} --bind http://127.0.0.1:{api_port}'
        self.result = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,encoding="gbk")
        while True:
            next_line = self.result.stdout.readline().strip()
            return_line = next_line
            if return_line == '' and self.result.poll() != None:
                break
            if return_line in [f"System.IO.IOException: Failed to bind to address http://127.0.0.1:{api_port}: address already in use.","System.Net.Sockets.SocketException (10013): 以一种访问权限不允许的方式做了一个访问套接字的尝试。","System.Net.Sockets.SocketException (10049): 在其上下文中，该请求的地址无效。"]:
                logger.error(f"录播姬出现错误:{return_line}")
            # if return_line in "Dispose called":
            #     logger.warning("录播姬关闭")
            #     Recorder__active = False
            #     break
        returncode = self.result.wait()
        if returncode and Recorder__active == True :
            logger.error(f"录播姬出现错误:{return_line}")

    def Upload(self):
        from taskslist import UPLOAD
        logger.debug("正在初始化上传模块")
        while self.up__active == True:
            task = UPLOAD.get(block = True)
            if not task:
                    break
            self.up.up_manege(task)

    def Transcode(self):
        from taskslist import TRANSCODE
        logger.debug("正在初始化转码模块")
        while self.Transcode__active == True:
                task = TRANSCODE.get(block = True)
                if not task:
                    break
                self.transcode.transcode_manege(task)

    def tasksDocter(self):
        """
        任务状态监控
        -----------

        在使用中难免出现错误导致线程退出，这个模块旨在监测退出的线程并且重启它们。
        """
        import time
        logger.debug("正在初始化任务线程监控模块")
        while self.tasksDocter__active == True:
            time.sleep(2)
            if not self._run_recorder.is_alive():
                logger.error("录播姬挂了")
                thisfunc = self.run_recorder
                thisfunc()

            if not self._run_transcode.is_alive():
                logger.error("转码线程挂了,重开")
                thisfunc = self.run_transcode
                thisfunc()

            if not self._run_upload.is_alive():
                logger.error("上传线程挂了,重开")
                thisfunc = self.run_upload()
                thisfunc()

            if not self._run_ws.is_alive():
                logger.error("ws线程挂了,重开")
                self._run_ws = Thread(target=self.ws.run,name="WS")
                self._run_ws.start()


    def monitor(self):
        import time,json
        def send(message):
            try:
                self.ws.send(json.dumps(message))
            except:
                logger.warning('ws推送失败，请检查网络连接')
        while self.monitor__active == True:
            time.sleep(5)
            send(infolist())
    """
    功能模块初始化
    -------------

    这个方法对于NGlive的一些常用功能进行初始化

    * transcodego 是用于转码的模块 它运行在一个名为 `Transcode` 的线程
    * upgo 是用于上传文件到云端的模块 它运行在一个名为 `Upload` 的线程
    * wsgo 是保持维护一个WebSocket 它主动向中心服务器推送各种信息 它运行在一个名为 `WS` 的线程
    * tasksDoc 是用来监测主要线程的模块，它可以重启出现致命性错误而退出的线程 它运行在一个名为 `tasksDocter` 的线程
    * monitor 是用于监测系统各项数据 发送心跳和服务器状态，是中心服务器判断集群成员健康情况的重要模块 它运行在一个名为 `Monitor` 的线程

    """
    def run_transcode(self):
        self._run_transcode = Thread(target=self.Transcode,name="Transcode")
        self._run_transcode.start()

    def run_upload(self):
        self._run_upload = Thread(target=self.Upload,name="Upload")
        self._run_upload.start()

    def run_ws(self):
        self._run_ws = Thread(target=self.ws.run,name="WS")
        self._run_ws.start()

    def run_recorder(self):
        self._run_recorder = Thread(target=self.Recorder,name="BiliRecorder")
        self._run_recorder.start()
    
    def run_tasksdocter(self):
        self._run_tasksdocter = Thread(target=self.tasksDocter,name="tasksDocter")
        self._run_tasksdocter.start()
    
    def run_monitor(self):
        self._run_monitor = Thread(target=self.monitor,name="Monitor")
        self._run_monitor.start()
        
    """
    关闭线程的方法 亚萨西的关闭
    它会在线程执行完毕当前任务的时候，才关闭掉
    """
    def stop_tasksdocter(self):
        self.tasksDocter__active = False
        # 等待事件处理线程退出
        self._run_tasksdocter.join()
        self.tasksDocter__active = True

    def stop_up(self):
        if UPLOAD.empty():
            UPLOAD.put(False)
        else:
            self.up__active = False
        self._run_upload.join()
        self.up__active = True

    def stop_transcode(self):
        if TRANSCODE.empty():
            TRANSCODE.put(False)
        else:
            self.Transcode__active = False
        self._run_transcode.join()
        self.Transcode__active = True

    def stop_recorder(self):
        self.result.terminate()

    def stop_ws(self):
        self.ws.ws.close()

    def stop_monitor(self):
        self.monitor__active = False
        self._run_monitor.join()
        self.monitor__active = True

    """
    强♂硬的关闭 不管他在干嘛 直接掐了
    不建议在一般场景使用这个，因为可能会带来一些意想不到的问题。
    """
    def kill_tasksdocter(self):
        logger.warning("正在强制关闭转码线程")
        stop_thread(self._run_transcode)
        logger.warning("强制关闭转码线程成功")

        

