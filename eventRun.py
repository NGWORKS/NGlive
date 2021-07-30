from os import name
from loguru import logger
from linstener import RecorderListener, TranscodeListener,UpListener
from threading import Thread
from eventManager import EventManager
from wsclient import *
from trcode import transcode
from up import up
import inspect
import ctypes
from log import logger
from systemInfo import get_sys_info

class NGlive:
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
        self.transcodego = Thread(target=self.transcode.transcode_manege,name="Transcode")
        # 上传模块
        self.upgo = Thread(target=self.up.up_manege,name="Upload")
        # ws上报模块
        self.wsgo = Thread(target=self.ws.run,name="WS")
        # 线程医生
        self.tasksDoc = Thread(target=self.tasksDocter,name="tasksDocter")
        # 系统监控
        self.monitor = Thread(target=get_sys_info,name="Monitor",args=(self.ws,))
    
    def tasksGo(self):
        logger.info("正在初始化任务线程")
        self.transcodego.start()
        self.upgo.start()
        self.wsgo.start()
        self.tasksDoc.start()
        self.monitor.start()
        logger.info("任务线程初始化成功")
    
    def tasksDocter(self):
        import time
        logger.debug("正在初始化任务线程监控模块")
        while True:
            time.sleep(2)
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
        

