"""
这个程序文件实现了启动相关线程、注册监听器、自我修复的功能

>> 启动各项功能
>> 注册相应的事件监听器
>> 提供系统状态监测、各线程工作状态监测

"""
from initial import NGhost
from os import name
from loguru import logger
from linstener import RecorderListener, TranscodeListener,UpListener
from threading import Thread
from eventManager import EventManager
from wsclient import *
from trcode import transcode
from up import up
import inspect
import ctypes,subprocess
from log import logger
from systemInfo import get_sys_info


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
        self.transcodego_tag = True

    
    def _async_raise(self,tid, exctype):
        """raises the exception, performs cleanup if needed"""
        print(tid)
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
    def stop_thread(self,thread):
        self._async_raise(thread.ident, SystemExit)
        
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
    
    def functionBlock(self):
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
        self.transcodego = Thread(target=self.transcode.transcode_manege,name="Transcode")
        # 上传模块
        self.upgo = Thread(target=self.up.up_manege,name="Upload")
        # ws上报模块
        self.wsgo = Thread(target=self.ws.run,name="WS")
        # 线程医生
        self.Recordergo = Thread(target=self.run_Recorder,name="BiliRecorder")
        self.tasksDoc = Thread(target=self.tasksDocter,name="tasksDocter")
        # 系统监控
        self.monitor = Thread(target=get_sys_info,name="Monitor",args=(self.ws,))
    
    def tasksGo(self):
        """
        启动线程
        -------
        这个方法实现了启动上述定义好的任务。
        """
        logger.info("正在初始化任务线程")
        self.transcodego.start()
        self.upgo.start()
        self.wsgo.start()
        self.tasksDoc.start()
        self.Recordergo.start()
        self.monitor.start()
        logger.info("任务线程初始化成功")

    def run_Recorder(self):
        logger.info("正在启动录播姬")
        from initial import RecorderPath,works_path,api_port
        cmd = f'"{RecorderPath}" run {works_path} --bind http://127.0.0.1:{api_port}'
        result = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,shell=True,encoding="gbk")
        while True:
            next_line = result.stdout.readline().strip()
            return_line = next_line
            if return_line == '' and result.poll() != None:
                break
            if return_line in [f"System.IO.IOException: Failed to bind to address http://127.0.0.1:{api_port}: address already in use.","System.Net.Sockets.SocketException (10013): 以一种访问权限不允许的方式做了一个访问套接字的尝试。","System.Net.Sockets.SocketException (10049): 在其上下文中，该请求的地址无效。"]:
                logger.error(f"录播姬出现错误:{return_line}")
                raise Exception(return_line)
            if return_line in "Dispose called":
                logger.error("录播姬意外关闭，原因未知")
                raise Exception(return_line)
        
        returncode = result.wait()
        if returncode:
            logger.error(f"录播姬出现错误:{return_line}")
            raise Exception(return_line)
                        
    def tasksDocter(self):
        """
        任务状态监控
        -----------

        在使用中难免出现错误导致线程退出，这个模块旨在监测退出的线程并且重启它们。
        """
        import time
        logger.debug("正在初始化任务线程监控模块")
        while True:
            time.sleep(2)
            if not self.Recordergo.is_alive():
                logger.error("录播姬挂了")
                self.Recordergo = Thread(target=self.run_Recorder,name="BiliRecorder")
                self.Recordergo.start()

            if not self.transcodego.is_alive() and self.transcodego_tag == False:
                logger.error("转码线程挂了,重开")
                self.transcodego = Thread(target=self.transcode.transcode_manege,name="Transcode")
                self.transcodego.start()

            if not self.upgo.is_alive():
                logger.error("上传线程挂了,重开")
                self.upgo = Thread(target=self.up.up_manege,name="Upload")
                self.upgo.start()

            if not self.wsgo.is_alive():
                logger.error("ws线程挂了,重开")
                self.wsgo = Thread(target=self.ws.run,name="WS")
                self.wsgo.start()
        

