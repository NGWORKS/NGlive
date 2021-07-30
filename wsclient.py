import websocket
from log import logger

ws_on = True


class wsc:
    def __init__(self) -> None:
        self.ws = None
        self.reconnect_count = 1


    def on_opend(self,ws):
        logger.debug('WS连接成功')

    def on_message(self,ws, message):
        #print(message)
        pass


    def on_close(self,ws):
        print("### closed ###")



    def send(self,message):
        self.ws.send(message)

    def on_error(self,ws, error):
        import time
        logger.error(f"WS连接出现错误，错误是：{error}")
        global reconnect_count
        time.sleep(1)
        logger.warning(f"正在尝试第{self.reconnect_count}次重连")
        self.reconnect_count+=1
        if self.reconnect_count<=100:
            self.run()
        else:
            logger.error("连接错误次数过多，已停用ws")
            self.reconnect_count = 1

    def run(self):
        logger.debug("正在初始化WS模块")
        websocket.enableTrace(False)
        ws = websocket.WebSocketApp("ws://lb.ngworks.cn/nglive/nglive_xa/ws?token=3b1e903e-1a8c-8fa8-296e-dbd9bfcc2e38",
                                    on_open= self.on_opend,
                                    on_message=self.on_message,
                                    on_error=self.on_error,
                                    on_close=self.on_close)

        self.ws = ws
        ws.run_forever()    
