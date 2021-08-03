import websocket
from log import logger
from initial import wspath
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
        logger.info("WS连接关闭")



    def send(self,message):
        self.ws.send(message)

    def on_error(self,ws, error):
        import time
        logger.error(f"WS连接出现错误，错误是：{error}")
        global reconnect_count
        time.sleep(1)
        logger.warning(f"正在尝试第{self.reconnect_count}次重连")
        self.reconnect_count+=1
        if self.reconnect_count<=10:
            self.run()
        else:
            logger.error("连接错误次数过多，已停用ws")
            self.reconnect_count = 1
            raise ConnectionError("ws连接失败次数过多")

    def run(self):
        websocket.enableTrace(False)
        ws = websocket.WebSocketApp(wspath,
                                    on_open= self.on_opend,
                                    on_message=self.on_message,
                                    on_error=self.on_error,
                                    on_close=self.on_close)

        self.ws = ws
        ws.run_forever()
