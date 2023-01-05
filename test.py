from leekquant.ths_trader import ThsTrader
from loguru import logger as log
from tabulate import tabulate
import time
import unittest

class ThsTraderTestCase(unittest.TestCase):

    def setUp(self):
        ip = '127.0.0.1'
        mark = 3721
        self.trader = ThsTrader(ip, mark)

    def test_get_position(self):
        """查询持仓 """
        log.info('测试: 查询持仓')
        start = time.time()*1000
        df = self.trader.get_position(to_dataframe=True)
        log.debug('\n{}', tabulate(df, headers='keys', tablefmt='psql'))
        log.debug('耗时: {}ms', int(time.time()*1000 - start))

    def test_get_balance(self):
        """查询资金账户"""
        log.info('测试: 查询资金账户')
        start = time.time()*1000
        d = self.trader.get_balance()
        log.debug('{}', d)
        log.debug('耗时: {}ms', int(time.time()*1000 - start))

    def test_get_today_trades(self):
        """查询今日成交"""
        log.info('测试: 查询今日成交')
        start = time.time()*1000
        df = self.trader.get_today_trades(to_dataframe=True)
        if not df.empty:
            log.debug('\n{}', tabulate(df, headers='keys', tablefmt='psql'))
        else:
            log.debug('无今日成交')
        log.debug('耗时: {}ms', int(time.time()*1000 - start))

    def test_get_today_entrusts(self):
        """查询今日委托"""
        log.info('测试: 查询今日委托')
        start = time.time()*1000
        df = self.trader.get_today_entrusts(to_dataframe=True)
        if not df.empty:
           log.debug('\n{}', tabulate(df, headers='keys', tablefmt='psql'))
        else:
            log.debug('无今日委托')
        log.debug('耗时: {}ms', int(time.time()*1000 - start))

    # def test_buy(self):
    #     """买入(防止实盘，先屏蔽)"""
    #     log.info('测试: 买入')
    #     res = self.trader.buy('513330', 0.311, 100)

    # def test_sell(self):
    #     log.info('测试: 卖出')
    #     res = self.trader.sell('513330', 1.11, 100)
    #     log.debug(res)

    # def test_cancel_buy(self):
    #     """撤买"""
    #     res = self.trader.cancel('buy')

    # def test_cancel_sell(self):
    #     """撤卖"""
    #     res = self.trader.cancel('sell')
    
    # def test_cancel_all(self):
    #     """撤所有"""
    #     res = self.trader.cancel('all')
    #     log.debug('撤单结果: {}', res)

if __name__ == "__main__":
    unittest.main()