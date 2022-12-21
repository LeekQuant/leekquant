import json
import socket
import time
import pandas as pd
import requests
import requests.packages.urllib3.util.connection as urllib3_conn
from loguru import logger as log

class ThsTrader:

    def __init__(self, ip, mark):
        log.info('init ths trader')
        pd.set_option('display.max_rows', None)
        urllib3_conn.allowed_gai_family = lambda: socket.AF_INET
        self.ip = ip
        self.mark = mark

    def get_position(self, to_dataframe=False):
        """获取仓位"""
        ret = self.__do('get_position')
        return pd.DataFrame(ret['data']) if to_dataframe else ret['data']

    def get_balance(self) -> dict:
        """账户资金情况"""
        return self.__do('get_balance')

    def get_today_trades(self, to_dataframe=False):
        """今日成交"""
        ret = self.__do('get_today_trades')
        return pd.DataFrame(ret['data']) if to_dataframe else ret['data']

    def get_today_entrusts(self, to_dataframe=False):
        """今日委托"""
        ret = self.__do('get_today_entrusts')
        return pd.DataFrame(ret['data']) if to_dataframe else ret['data']

    def buy(self, code:str, price:float, num:int):
        """
        下单买入
        :param code: 6位数代码
        :param price: 交易价格
        :param num: 买入数量
        """
        payload = [str(code), price, num]
        ret = self.__do('buy', payload)
        res_msg = ret['data'] if 'data' in ret.keys() else ''
        contract = self.__get_contract(res_msg)
        return res_msg if contract == '' else contract
    
    def sell(self, code:str, price:float, num:int):
        """
        下单卖出
        :param code: 6位数代码
        :param price: 交易价格
        :param num: 卖出数量
        """
        ret = self.__do('sell', [str(code), price, num])
        res_msg = ret['data'] if 'data' in ret.keys() else ''
        contract = self.__get_contract(res_msg)
        return res_msg if contract == '' else contract

    def cancel(self, op:str):
        # {"code":0,"data":"无可撤委托"}
        if op not in ['buy', 'sell', 'all']:
            raise Exception('非法的参数op, op支持: buy(撤买)|sell(撤卖)|all(撤所有)')
        ret = self.__do('cancel_entrust', [op])
        return ret['data'] if 'data' in ret.keys() else ''

    def __do(self, op, data={}):
        url = 'http://%s:%d/api/%s' % (self.ip, self.mark, op)
        res = requests.post(url, json=data, headers = {'Content-Type': 'application/json'})
        res.encoding = 'gb2312'
        if res.status_code != 200:
            raise Exception('无法获取数据, 下单程序运行正常?')

        # print(res.text)
        ret = res.json()
        if ret['code'] != 0:
            raise Exception('下单程序出错了, 原因: %s' % self.__get_msg(ret['code']))
        return ret
  
    def __get_msg(self, code):
        errors = {
            1001: '未登录',
            1002: '超时, 掉线了?',
            1003: '内部错误',
            1004: '参数不正确'
        }
        return errors[code] if errors.__contains__(code) else "未知错误"

    def __get_contract(self, res_msg):
        """
        获取返回结果中的合同编号
        :param res_msg: 弹出框的具体信息，例如: 您的买入委托已成功提交，合同编号：865912566。
        """
        if res_msg is None or len(res_msg) == 0:
            return ''
        try:
            return res_msg.split("合同编号：")[1].split("。")[0]
        except:
            pass