import requests
from initial import api_port

def getRooms():
    weburl = f"http://127.0.0.1:{api_port}/graphql?query=query%20MyQuery%20%7B%0A%20%20rooms%20%7B%0A%20%20%20%20areaNameChild%0A%20%20%20%20areaNameParent%0A%20%20%20%20autoRecordForThisSession%0A%20%20%20%20danmakuConnected%0A%20%20%20%20name%0A%20%20%20%20objectId%0A%20%20%20%20recording%0A%20%20%20%20shortId%0A%20%20%20%20streaming%0A%20%20%20%20title%0A%20%20%20%20roomConfig%20%7B%0A%20%20%20%20%20%20autoRecord%0A%20%20%20%20%20%20roomId%0A%20%20%20%20%20%20optionalCuttingMode%20%7B%0A%20%20%20%20%20%20%20%20hasValue%0A%20%20%20%20%20%20%20%20value%0A%20%20%20%20%20%20%7D%0A%20%20%20%20%20%20optionalCuttingNumber%20%7B%0A%20%20%20%20%20%20%20%20hasValue%0A%20%20%20%20%20%20%20%20value%0A%20%20%20%20%20%20%7D%0A%20%20%20%20%20%20optionalRecordDanmaku%20%7B%0A%20%20%20%20%20%20%20%20value%0A%20%20%20%20%20%20%20%20hasValue%0A%20%20%20%20%20%20%7D%0A%20%20%20%20%20%20optionalRecordDanmakuGift%20%7B%0A%20%20%20%20%20%20%20%20hasValue%0A%20%20%20%20%20%20%20%20value%0A%20%20%20%20%20%20%7D%0A%20%20%20%20%20%20optionalRecordDanmakuGuard%20%7B%0A%20%20%20%20%20%20%20%20hasValue%0A%20%20%20%20%20%20%20%20value%0A%20%20%20%20%20%20%7D%0A%20%20%20%20%20%20optionalRecordDanmakuRaw%20%7B%0A%20%20%20%20%20%20%20%20hasValue%0A%20%20%20%20%20%20%20%20value%0A%20%20%20%20%20%20%7D%0A%20%20%20%20%20%20optionalRecordDanmakuSuperChat%20%7B%0A%20%20%20%20%20%20%20%20hasValue%0A%20%20%20%20%20%20%20%20value%0A%20%20%20%20%20%20%7D%0A%20%20%20%20%20%20optionalRecordMode%20%7B%0A%20%20%20%20%20%20%20%20hasValue%0A%20%20%20%20%20%20%20%20value%0A%20%20%20%20%20%20%7D%0A%20%20%20%20%7D%0A%20%20%20%20stats%20%7B%0A%20%20%20%20%20%20duraionRatio%0A%20%20%20%20%20%20fileMaxTimestamp%0A%20%20%20%20%20%20networkMbps%0A%20%20%20%20%20%20sessionDuration%0A%20%20%20%20%20%20sessionMaxTimestamp%0A%20%20%20%20%20%20totalInputBytes%0A%20%20%20%20%20%20totalOutputBytes%0A%20%20%20%20%7D%0A%20%20%7D%0A%7D&variables=%7B%7D&operationName=MyQuery"
    r = requests.get(weburl)
    return r.json()

def getRoom(roomid:int,objectId:str):
    weburl = f"http://127.0.0.1:{api_port}/graphql?query=query%20MyQuery%20%7B%0A%20%20room(objectId:%20%22{objectId}%22,%20roomId:%20{roomid})%20%7B%0A%20%20%20%20areaNameChild%0A%20%20%20%20areaNameParent%0A%20%20%20%20autoRecordForThisSession%0A%20%20%20%20danmakuConnected%0A%20%20%20%20name%0A%20%20%20%20objectId%0A%20%20%20%20recording%0A%20%20%20%20shortId%0A%20%20%20%20streaming%0A%20%20%20%20title%0A%20%20%20%20stats%20%7B%0A%20%20%20%20%20%20duraionRatio%0A%20%20%20%20%20%20fileMaxTimestamp%0A%20%20%20%20%20%20networkMbps%0A%20%20%20%20%20%20sessionDuration%0A%20%20%20%20%20%20sessionMaxTimestamp%0A%20%20%20%20%20%20totalInputBytes%0A%20%20%20%20%20%20totalOutputBytes%0A%20%20%20%20%7D%0A%20%20%20%20roomConfig%20%7B%0A%20%20%20%20%20%20autoRecord%0A%20%20%20%20%20%20optionalCuttingMode%20%7B%0A%20%20%20%20%20%20%20%20hasValue%0A%20%20%20%20%20%20%20%20value%0A%20%20%20%20%20%20%7D%0A%20%20%20%20%20%20optionalCuttingNumber%20%7B%0A%20%20%20%20%20%20%20%20hasValue%0A%20%20%20%20%20%20%20%20value%0A%20%20%20%20%20%20%7D%0A%20%20%20%20%20%20optionalRecordDanmaku%20%7B%0A%20%20%20%20%20%20%20%20hasValue%0A%20%20%20%20%20%20%20%20value%0A%20%20%20%20%20%20%7D%0A%20%20%20%20%20%20optionalRecordDanmakuGift%20%7B%0A%20%20%20%20%20%20%20%20hasValue%0A%20%20%20%20%20%20%20%20value%0A%20%20%20%20%20%20%7D%0A%20%20%20%20%20%20optionalRecordDanmakuGuard%20%7B%0A%20%20%20%20%20%20%20%20hasValue%0A%20%20%20%20%20%20%20%20value%0A%20%20%20%20%20%20%7D%0A%20%20%20%20%20%20optionalRecordDanmakuRaw%20%7B%0A%20%20%20%20%20%20%20%20hasValue%0A%20%20%20%20%20%20%20%20value%0A%20%20%20%20%20%20%7D%0A%20%20%20%20%20%20optionalRecordDanmakuSuperChat%20%7B%0A%20%20%20%20%20%20%20%20hasValue%0A%20%20%20%20%20%20%20%20value%0A%20%20%20%20%20%20%7D%0A%20%20%20%20%20%20roomId%0A%20%20%20%20%20%20optionalRecordMode%20%7B%0A%20%20%20%20%20%20%20%20hasValue%0A%20%20%20%20%20%20%20%20value%0A%20%20%20%20%20%20%7D%0A%20%20%20%20%7D%0A%20%20%7D%0A%7D&variables=%7B%7D&operationName=MyQuery"
    r = requests.get(weburl)
    return r.json()

def addRoom(roomid:int):
    weburl = f"http://127.0.0.1:{api_port}/graphql?query=mutation%20MyMutation%20%7B%0A%20%20__typename%0A%20%20addRoom(autoRecord:%20true,%20roomId:%20{roomid})%20%7B%0A%20%20%20%20areaNameChild%0A%20%20%20%20areaNameParent%0A%20%20%20%20autoRecordForThisSession%0A%20%20%20%20name%0A%20%20%20%20danmakuConnected%0A%20%20%20%20objectId%0A%20%20%20%20recording%0A%20%20%20%20roomConfig%20%7B%0A%20%20%20%20%20%20autoRecord%0A%20%20%20%20%20%20optionalCuttingMode%20%7B%0A%20%20%20%20%20%20%20%20hasValue%0A%20%20%20%20%20%20%20%20value%0A%20%20%20%20%20%20%7D%0A%20%20%20%20%20%20optionalCuttingNumber%20%7B%0A%20%20%20%20%20%20%20%20hasValue%0A%20%20%20%20%20%20%20%20value%0A%20%20%20%20%20%20%7D%0A%20%20%20%20%20%20optionalRecordDanmaku%20%7B%0A%20%20%20%20%20%20%20%20hasValue%0A%20%20%20%20%20%20%20%20value%0A%20%20%20%20%20%20%7D%0A%20%20%20%20%20%20optionalRecordDanmakuGift%20%7B%0A%20%20%20%20%20%20%20%20hasValue%0A%20%20%20%20%20%20%20%20value%0A%20%20%20%20%20%20%7D%0A%20%20%20%20%20%20optionalRecordDanmakuGuard%20%7B%0A%20%20%20%20%20%20%20%20hasValue%0A%20%20%20%20%20%20%20%20value%0A%20%20%20%20%20%20%7D%0A%20%20%20%20%20%20optionalRecordDanmakuRaw%20%7B%0A%20%20%20%20%20%20%20%20hasValue%0A%20%20%20%20%20%20%20%20value%0A%20%20%20%20%20%20%7D%0A%20%20%20%20%20%20optionalRecordDanmakuSuperChat%20%7B%0A%20%20%20%20%20%20%20%20hasValue%0A%20%20%20%20%20%20%20%20value%0A%20%20%20%20%20%20%7D%0A%20%20%20%20%20%20optionalRecordMode%20%7B%0A%20%20%20%20%20%20%20%20hasValue%0A%20%20%20%20%20%20%20%20value%0A%20%20%20%20%20%20%7D%0A%20%20%20%20%20%20roomId%0A%20%20%20%20%7D%0A%20%20%20%20shortId%0A%20%20%20%20stats%20%7B%0A%20%20%20%20%20%20duraionRatio%0A%20%20%20%20%20%20fileMaxTimestamp%0A%20%20%20%20%20%20networkMbps%0A%20%20%20%20%20%20sessionDuration%0A%20%20%20%20%20%20sessionMaxTimestamp%0A%20%20%20%20%20%20totalInputBytes%0A%20%20%20%20%20%20totalOutputBytes%0A%20%20%20%20%7D%0A%20%20%20%20streaming%0A%20%20%20%20title%0A%20%20%7D%0A%7D&variables=%7B%7D&operationName=MyMutation"
    r = requests.get(weburl)
    return r.json()

def removeRoom(roomid:int,objectId:str):
    weburl = f"http://127.0.0.1:{api_port}/graphql?query=mutation%20MyMutation%20%7B%0A%20%20__typename%0A%20%20removeRoom(objectId:%20%22{objectId}%22,%20roomId:%20{roomid})%20%7B%0A%20%20%20%20areaNameChild%0A%20%20%20%20areaNameParent%0A%20%20%20%20name%0A%20%20%20%20objectId%0A%20%20%20%20shortId%0A%20%20%20%20title%0A%20%20%20%20roomConfig%20%7B%0A%20%20%20%20%20%20roomId%0A%20%20%20%20%20%20autoRecord%0A%20%20%20%20%7D%0A%20%20%7D%0A%7D&variables=%7B%7D&operationName=MyMutation"
    r = requests.get(weburl)
    return r.json()

def stopRecording(roomid:int,objectId:str):
    weburl = f"http://127.0.0.1:{api_port}/graphql?query=mutation%20MyMutation%20%7B%0A%20%20__typename%0A%20%20stopRecording(objectId:%20%22{objectId}%22,%20roomId:%20{roomid})%20%7B%0A%20%20%20%20areaNameChild%0A%20%20%20%20areaNameParent%0A%20%20%20%20danmakuConnected%0A%20%20%20%20name%0A%20%20%20%20objectId%0A%20%20%20%20shortId%0A%20%20%20%20title%0A%20%20%7D%0A%7D&variables=%7B%7D&operationName=MyMutation"
    r = requests.get(weburl)
    return r.json()

def startRecording(roomid:int,objectId:str):
    weburl = f"http://127.0.0.1:{api_port}/graphql?query=mutation%20MyMutation%20%7B%0A%20%20__typename%0A%20%20startRecording(objectId:%20%22{objectId}%22,%20roomId:%20{roomid})%20%7B%0A%20%20%20%20areaNameChild%0A%20%20%20%20areaNameParent%0A%20%20%20%20danmakuConnected%0A%20%20%20%20name%0A%20%20%20%20objectId%0A%20%20%20%20shortId%0A%20%20%20%20title%0A%20%20%7D%0A%7D&variables=%7B%7D&operationName=MyMutation"
    r = requests.get(weburl)
    return r.json()

def refreshRoom(roomid:int,objectId:str):
    weburl = f"http://127.0.0.1:{api_port}/graphql?query=mutation%20MyMutation%20%7B%0A%20%20__typename%0A%20%20refreshRoomInfo(objectId:%20%22{objectId}%22,%20roomId:%20{roomid})%20%7B%0A%20%20%20%20areaNameChild%0A%20%20%20%20autoRecordForThisSession%0A%20%20%20%20areaNameParent%0A%20%20%20%20danmakuConnected%0A%20%20%20%20name%0A%20%20%20%20objectId%0A%20%20%20%20recording%0A%20%20%20%20roomConfig%20%7B%0A%20%20%20%20%20%20autoRecord%0A%20%20%20%20%20%20roomId%0A%20%20%20%20%20%20optionalCuttingMode%20%7B%0A%20%20%20%20%20%20%20%20hasValue%0A%20%20%20%20%20%20%20%20value%0A%20%20%20%20%20%20%7D%0A%20%20%20%20%20%20optionalCuttingNumber%20%7B%0A%20%20%20%20%20%20%20%20hasValue%0A%20%20%20%20%20%20%20%20value%0A%20%20%20%20%20%20%7D%0A%20%20%20%20%20%20optionalRecordDanmaku%20%7B%0A%20%20%20%20%20%20%20%20hasValue%0A%20%20%20%20%20%20%20%20value%0A%20%20%20%20%20%20%7D%0A%20%20%20%20%20%20optionalRecordDanmakuGift%20%7B%0A%20%20%20%20%20%20%20%20hasValue%0A%20%20%20%20%20%20%20%20value%0A%20%20%20%20%20%20%7D%0A%20%20%20%20%20%20optionalRecordDanmakuGuard%20%7B%0A%20%20%20%20%20%20%20%20hasValue%0A%20%20%20%20%20%20%20%20value%0A%20%20%20%20%20%20%7D%0A%20%20%20%20%20%20optionalRecordDanmakuRaw%20%7B%0A%20%20%20%20%20%20%20%20hasValue%0A%20%20%20%20%20%20%20%20value%0A%20%20%20%20%20%20%7D%0A%20%20%20%20%20%20optionalRecordDanmakuSuperChat%20%7B%0A%20%20%20%20%20%20%20%20hasValue%0A%20%20%20%20%20%20%20%20value%0A%20%20%20%20%20%20%7D%0A%20%20%20%20%20%20optionalRecordMode%20%7B%0A%20%20%20%20%20%20%20%20hasValue%0A%20%20%20%20%20%20%20%20value%0A%20%20%20%20%20%20%7D%0A%20%20%20%20%7D%0A%20%20%20%20shortId%0A%20%20%20%20streaming%0A%20%20%20%20title%0A%20%20%7D%0A%7D&variables=%7B%7D&operationName=MyMutation"
    r = requests.get(weburl)
    return r.json()

if __name__ =="__main__":
    # 查看所有房间信息
    allroom = getRooms()

    Rooms = allroom['data']['rooms']
    for room in Rooms:
        print(room)

    # print("-------------------------------------")

    # # 查看指定房间信息
    # thisroom = getRoom(roomId,objectId)
    # print(thisroom)
    # print("-------------------------------------")

    # # 添加房间
    # room = 21292831
    # therroomconf = addRoom(room)
    # print(therroomconf)
    # objectId = therroomconf['data']['addRoom']['objectId']
    # print("-------------------------------------")

    # # 开始录制
    # start = startRecording(21292831,"b65a39ed-f4de-43a2-bf13-78c9c32369ee")
    # print(start)
    # print("-------------------------------------")

    # # 停止录制
    # stop = stopRecording(21292831,"b65a39ed-f4de-43a2-bf13-78c9c32369ee")
    # print(stop)
    # print("-------------------------------------")

    # # 移除房间
    # delcallback = removeRoom(21292831,"b65a39ed-f4de-43a2-bf13-78c9c32369ee")
    # print(delcallback)
    


