
from baidupcs_py import commands
from baidupcs_py.baidupcs import BaiduPCSApi, api
from baidupcs_py.commands import share
from upload import upload,from_tos
from taskslist import UPLOAD
from eventManager import Event
from resquest_test import TtranscodeOut
from pathlib import Path

from db import RecorderDB,Rate
from log import logger



def extract_cookies(cookie):
    cookies = dict([l.split("=", 1) for l in cookie.split("; ")])
    return cookies

def getpwd():
    str1 = '1234567890qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM'
    import random
    while True:
        code=''
        for i in range(4):
            num = random.randint(0,len(str1)-1)
            code += str1[num]
        return code


B = BaiduPCSApi(cookies=extract_cookies(cookies),bduss=bduss)
class up:
    def __init__(self,eventManager):
        self.__eventManager = eventManager

    def sendEvent(self,msg,**dt):
        event = Event(type_=msg)
        event.dict["artical"] = TtranscodeOut(**dt)
        self.__eventManager.SendEvent(event)
    
    def upf(self,localpaths, remotedir,id):
        ft = from_tos([localpaths],remotedir)
        upload(api=B,show_progress=False,from_to_list=ft,_tid=id,eventManager=self.__eventManager)
    
    def up_manege(self):
        logger.debug("正在初始化上传模块")
        while True:
            task = UPLOAD.get(block=True)
            self.sendEvent("UpStarted",tasksid = task.TaskId)
            print(task)
            upfile = task.OutPut
            if task.OutPut is None or task.Transcode is not True:
                print("mriy")
                upfile = task.Origin
            clouldpath = "/vup/"
            self.upf(upfile ,clouldpath ,task.TaskId)
            password = getpwd()
            period=7
            logger.debug(f"上传子任务完毕")
            clouldfilepath = f"{clouldpath}{Path(upfile).name}"
            shared_link = B.share(clouldfilepath, password=password, period=period)
            logger.info(f"分享链接{shared_link.url}，密码{password}，有效期{period}天。")
            with RecorderDB(Rate) as f:
                Ratedata = f.filter(TaskId = task.TaskId)[0]
                Ratedata.Clould = clouldfilepath
                Ratedata.ShareUrl = shared_link.url
                Ratedata.SharePwd = password








