import socketio
import json
import time
import threading
from loguru import logger as log

class Quote:
    def __init__(self, token=''):
        self.token = token
        self.quote_url = 'http://47.242.67.95:8000/'
        # self.quote_url = 'http://127.0.0.1:8000/'
        self.targets = []

        self.tick_handler = None
        self.overview_handler = None

        self.sio = socketio.Client()
        self.sio.on('connect', self.connect)
        self.sio.on('connect_error', self.connect_error)
        self.sio.on('disconnect', self.disconnect)
        self.sio.on('tick', self.on_tick)
        self.sio.on('overview', self.on_overview)
        self.__connect()

    def sub_tick(self, codes=[]):
        if len(codes) == 0: return
        log.debug('订阅TICK: {}', codes)
        self.sio.emit('sub-tick', json.dumps(codes))

    def unsub_tick(self, codes=[]):
        if len(codes) == 0: return
        log.debug('取消订阅TICK: {}', codes)
        self.sio.emit('unsub-tick', json.dumps(codes))

    def sub_overview(self):
        log.debug('订阅市场概况')
        self.sio.emit('overview')
    
    def connect(self):
        log.debug('connection established')

    def connect_error(self, err):
        log.warning(err)
        raise("连接出错啦:", err)
        
    def disconnect(self):
        log.debug('disconnected from server')

    def on_tick(self, tick):
        if self.sio.connected and self.tick_handler is not None:
            # self.tick_handler(tick)
            threading.Thread(target = self.tick_handler, args = (tick,)).start()
    
    def on_overview(self, tick):
        if self.sio.connected and self.overview_handler is not None:
            # self.overview_handler(tick)
            threading.Thread(target = self.overview_handler, args = (tick,)).start()

    def reg_tick_handler(self, handler):
        self.tick_handler = handler
    
    def reg_overview_handler(self, handler):
        self.overview_handler = handler

    def __connect(self):
        threading.Thread(target = lambda: (
            self.sio.connect(self.quote_url, auth={'token': self.token}),
            self.sio.wait()
        )).start()
        while not self.sio.connected:
            print('等待建立连接...')
            time.sleep(1)
            
if __name__ == '__main__':
    q = Quote()

    # =================== 订阅TICK ================== #
    # 定义并注册一个tick回调
    def tick_handler(tick):
        print('收到TICK:', tick)
    q.reg_tick_handler(tick_handler)
    # 订阅具体的代码，最多20个标的
    codes = '603690.SH,002371.SZ,300812.SZ'
    q.sub_tick(codes=codes.split(','))

    # =================== 订阅市场概况 ================= #
    def overview_handler(data):
        print('收到市场概况:', data)
    q.reg_overview_handler(overview_handler)
    q.sub_overview()
