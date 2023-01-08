import socketio
import json
import time
import threading
from loguru import logger as log

class Quote:
    def __init__(self, token=''):
        self.token = token
        self.quote_url = 'http://47.242.67.95:8000/'
        self.targets = []
        self.handler = None

        self.sio = socketio.Client()
        self.sio.on('connect', self.connect)
        self.sio.on('connect_error', self.connect_error)
        self.sio.on('disconnect', self.disconnect)
        self.sio.on('tick', self.on_tick)
        self.__connect()

    def sub_tick(self, codes=[]):
        if len(codes) == 0: return
        log.debug('订阅TICK:', codes)
        self.sio.emit('sub-tick', json.dumps(codes), namespace='/')

    def unsub_tick(self, codes=[]):
        if len(codes) == 0: return
        log.debug('取消订阅TICK:', codes)
        self.sio.emit('unsub-tick', json.dumps(codes), namespace='/')

    def sub_overview(self):
        self.sio.emit('sub-overview', namespace='/')
    
    def unsub_overview(self):
        self.sio.emit('unsub-overview', namespace='/')

    def connect(self):
        log.debug('connection established')

    def connect_error(self, err):
        log.warning(err)
        raise("连接出错啦:", err)
        
    def disconnect(self):
        log.debug('disconnected from server')

    def on_tick(self, tick):
        if self.sio.connected and self.handler is not None:
            # log.debug('TICK:', tick)
            self.handler(tick)

    def reg_tick_handler(self, handler):
        self.handler = handler

    def __connect(self):
        threading.Thread(target = lambda: (
            self.sio.connect(self.quote_url, namespaces=['/'], auth={'token': self.token}),
            self.sio.wait()
        )).start()    

if __name__ == '__main__':
    q = Quote()
    time.sleep(1)

    # 定义并注册一个tick回调
    def tick_handler(tick):
        print(tick)
    q.reg_tick_handler(tick_handler)

    # 订阅具体的代码，最多5个标的，注意格式
    codes = '603690.SH,002371.SZ,300812.SZ,300604.SZ,003043.SZ'
    q.sub_tick(codes=codes.split(','))