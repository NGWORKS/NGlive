from types import resolve_bases
from fastapi import FastAPI, BackgroundTasks
import time,os,asyncio
from eventManager import Event
from resquest_test import Webhook
from db import RecorderDB,Recorder
from __GraphQL import *
from eventRun import NGlive
from log import logger
from taskslist import Save_list,Load_list


NGlive = NGlive()

async def eventGo():
    from initial import NGhost, NGport
    Load_list()

    logger.info("正在初始化")
    funcs = [
        NGlive.ListenerImport,
        NGlive.run_recorder,
        NGlive.run_transcode,
        NGlive.run_upload,
        NGlive.run_ws,
        NGlive.run_tasksdocter,
        NGlive.run_monitor
    ]
    for func in funcs:
        newfunc = func
        newfunc()

    logger.info("初始化成功")
    logger.info("检查webhook配置")
    await asyncio.sleep(3)
    res = getWebHook()
    hasurl = res["data"]["config"]["optionalWebHookUrlsV2"]["hasValue"]
    url = res["data"]["config"]["optionalWebHookUrlsV2"]["value"]
    isurl = f"http://{NGhost}:{NGport}/webhook/"
    if hasurl is False or url != isurl:
        logger.info("webhook有误 进行配置")
        setWebHookV2(isurl)
    logger.info("webhook配置检查完毕")

def eventStop():
    logger.info("正在执行退出")
    logger.info("正在关闭线程监测模块")
    NGlive.stop_tasksdocter()
    logger.info("正在关闭上传模块")
    NGlive.stop_up()
    logger.info("正在关闭转码模块")
    NGlive.stop_transcode()
    logger.info("正在关闭录播姬")
    NGlive.stop_recorder()
    logger.info("正在关闭系统信息上报模块")
    NGlive.stop_monitor()
    logger.info("正在注销监听器")
    NGlive.eventManager.Stop()
    Save_list()
    logger.info("正在关闭ws模块")
    NGlive.stop_ws()
    logger.warning("感谢使用！再见~")

app = FastAPI(on_startup=[eventGo],on_shutdown=[eventStop])

def timetr(timestr):
    return time.mktime(time.strptime(timestr,'%Y-%m-%dT%H:%M:%S'))

def Event_Sender(Data: object):
    event = Event(type_=Data.EventType)
    event.dict["artical"] = Data
    NGlive.eventManager.SendEvent(event)
    EventData = Data.EventData

    with RecorderDB(Recorder) as f:
        f.add(
            EventId = Data.EventId, 
            SessionId = EventData.SessionId, 
            EventType = Data.EventType, 
            RoomId = EventData.RoomId, 
            ShortId = EventData.ShortId, 
            Name = EventData.Name, 
            Title = EventData.Title,
            RelativePath = EventData.RelativePath, 
            FileOpenTime = EventData.FileOpenTime, 
            FileCloseTime = EventData.FileCloseTime, 
            FileSize = EventData.FileSize, 
            Duration = EventData.Duration
        )


@app.post("/webhook/")
async def create_item(item: Webhook, background_tasks: BackgroundTasks):
    background_tasks.add_task(Event_Sender, item)
    return "ok"

@app.get("/addroom")
async def add_room(roomid:int):
    # 使用直播间号码 支持短号
    if roomid <= 0:
        return {"code":"4031","msg":"不正确的房间号"}
    allroominfo = getRooms()
    for room in allroominfo["data"]["rooms"]:
        objectId = room["objectId"]
        roomId = room["roomConfig"]["roomId"]
        shortId = room["shortId"]
        if roomId == roomid or shortId == roomid:
            return {"code":4032,"msg":"房间已经存在"}
    
    res = addRoom(roomid)
    res = refreshRoom(res["data"]["addRoom"]["roomConfig"]["roomId"],res["data"]["addRoom"]["objectId"])
    return {"code":0,"data":res["data"]["refreshRoomInfo"]}

@app.get("/removeroom")
async def remove_Room(roomid:int):
    # 查看这个房间号有没有在这里
    if roomid <= 0:
        return {"code":"4031","msg":"不正确的房间号"}
    allroominfo = getRooms()
    for room in allroominfo["data"]["rooms"]:
        recording = room["recording"]
        objectId = room["objectId"]
        roomId = room["roomConfig"]["roomId"]
        shortId = room["shortId"]
        if roomId == roomid or shortId == roomid:
            if recording:
                # 这个人人还在播，先给他掐了
                stopRecording(roomid,objectId)
            # 然后再移出录播列表
            await asyncio.sleep(2)
            res = removeRoom(roomid,objectId)
            return {"code":0,"data":res["data"]["removeRoom"]}
    return {"code":4042,"msg":"没有这个房间哦"}

@app.get("/allroom")
async def all_Room():
    res = getRooms()
    res["code"] = 0
    return res

@app.get("/getroom")
async def get_Room(roomid:int):
    # 查看这个房间号有没有在这里
    if roomid <= 0:
        return {"code":"4031","msg":"不正确的房间号"}
    allroominfo = getRooms()
    for room in allroominfo["data"]["rooms"]:
        roomId = room["roomConfig"]["roomId"]
        shortId = room["shortId"]
        if roomId == roomid or shortId == roomid:
            return {"code":0,"data":room}
    return {"code":4042,"msg":"没有这个房间哦"}

async def webend():

    logger.info("正在执行退出")
    logger.info("正在关闭线程监测模块")
    NGlive.stop_tasksdocter()
    logger.info("正在关闭系统信息上报模块")
    NGlive.stop_monitor()
    logger.info("正在关闭上传模块")
    NGlive.stop_up()
    logger.info("正在关闭转码模块")
    NGlive.stop_transcode()

    allroominfo = getRooms()
    for room in allroominfo["data"]["rooms"]:
        recording = room["recording"]
        objectId = room["objectId"]
        roomId = room["roomConfig"]["roomId"]
        if recording:
            logger.debug(f"{roomId}正在直播，现将其关闭。")
            stopRecording(roomId,objectId)
            await asyncio.sleep(10)
    Save_list()
    logger.info("正在关闭录播姬")
    NGlive.stop_recorder()
    logger.info("正在关闭ws模块")
    NGlive.stop_ws()


@app.get("/kill")
async def kill_up(background_tasks: BackgroundTasks):
    background_tasks.add_task(webend)
    return "呦西"

@app.get("/run")
async def run():
    from initial import NGhost, NGport
    Load_list()
    logger.info("正在初始化")
    funcs = [
        NGlive.run_recorder,
        NGlive.run_transcode,
        NGlive.run_upload,
        NGlive.run_ws,
        NGlive.run_tasksdocter,
        NGlive.run_monitor
    ]
    for func in funcs:
        newfunc = func
        newfunc()

    logger.info("初始化成功")
    logger.info("检查webhook配置")
    await asyncio.sleep(2)
    res = getWebHook()
    hasurl = res["data"]["config"]["optionalWebHookUrlsV2"]["hasValue"]
    url = res["data"]["config"]["optionalWebHookUrlsV2"]["value"]
    isurl = f"http://{NGhost}:{NGport}/webhook/"
    if hasurl is False or url != isurl:
        logger.info("webhook有误 进行配置")
        setWebHookV2(isurl)
    logger.info("webhook配置检查完毕")

    return "呦西"


if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app='api:app', host="127.0.0.1",
                port=8100, reload=False, debug=False)
