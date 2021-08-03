from logging import error
from baidupcs_py import commands
from baidupcs_py.baidupcs import BaiduPCSApi, api
from baidupcs_py.commands import share
from pydantic.main import EXTRA_LINK
from upload import upload,from_tos
from taskslist import UPLOAD
from eventManager import Event
from resquest_test import TtranscodeOut
from pathlib import Path

from db import RecorderDB,Rate
from log import logger

up__active = True


# 请参阅 baidupcs_py 自行更改 cookies bduss
from password import cookies,bduss



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



class up:
    def __init__(self,eventManager):
        self.__eventManager = eventManager
        self.__active = True
        try:
            self.API = BaiduPCSApi(cookies=extract_cookies(cookies),bduss=bduss)
        except:
            logger.error("百度网盘登录出现问题")

    def sendEvent(self,msg,**dt):
        event = Event(type_=msg)
        event.dict["artical"] = TtranscodeOut(**dt)
        self.__eventManager.SendEvent(event)
    
    def upf(self,localpaths, remotedir,id):
        ft = from_tos([localpaths],remotedir)
        upload(api=self.API,show_progress=False,from_to_list=ft,_tid=id,eventManager=self.__eventManager)

    def up_manege(self,task):
        self.sendEvent("UpStarted",tasksid = task.TaskId)
        upfile = task.OutPut
        if task.OutPut is None or task.Transcode is not True:
            upfile = task.Origin
        clouldpath = "/vup/"
        self.upf(upfile ,clouldpath ,task.TaskId)
        password = getpwd()
        period=7
        logger.debug(f"上传子任务完毕")
        clouldfilepath = f"{clouldpath}{Path(upfile).name}"
        shared_link = self.API.share(clouldfilepath, password=password, period=period)
        logger.info(f"分享链接{shared_link.url}，密码{password}，有效期{period}天。")
        with RecorderDB(Rate) as f:
            Ratedata = f.filter(TaskId = task.TaskId)[0]
            Ratedata.Clould = clouldfilepath
            Ratedata.ShareUrl = shared_link.url
            Ratedata.SharePwd = password

    def __exit__(self, exc_type, exc_value, exc_tb):
        if exc_type:
            print(f'exc_type: {exc_type}')
            print(f'exc_value: {exc_value}')
            print(f'exc_traceback: {exc_tb}')
            print('exception handled')
        return True 








