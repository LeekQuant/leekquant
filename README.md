## SLOGAN
让韭菜的股票量化变得更加简单

## 声明
仅限韭菜们自娱自乐, 勿用于商业用途, 亏钱和作者无关 :-)

## 缘起
* 目前韭菜的量化门槛太高，虽然有很多很好的量化平台，但是要么门槛高，要么手续费高
* 开源的几个THS下单都有各种各样的问题，维护都不是很及时
* 受益于此项目[thsauto](https://github.com/match5/thsauto)启发，实现一个类似的`REST`接口，方便各种语言接入

## 项目功能
* `选股` => `行情` => `下单`, 全流程闭环支持
* 选股基于`问财`, 用法参考 `usage_wencai.ipynb`
* 基于level1的实时行情推送，用法参考 `usage_quote.ipynb`
* 基于[韭菜下单](https://github.com/LeekQuant/leekquant/wiki/%E9%9F%AD%E8%8F%9C%E4%B8%8B%E5%8D%95%E6%93%8D%E4%BD%9C%E8%AF%B4%E6%98%8E)的自动下单软件，用法参考 `usage_trader.ipynb`

## REST接口
其他语言需要接入，请参考Wiki中[Rest接口](https://github.com/LeekQuant/leekquant/wiki/Rest%E6%8E%A5%E5%8F%A3)

## 运行项目
### **创建虚拟环境**
> conda create -n leekquant python=3.7
### 激活虚拟环境
> conda activate leekquant
### 安装依赖
> pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple/
### 用法参考测试用例
- 交易相关参考: `usage_trader.ipynb`
- 问财相关参考: `usage_wencai.ipynb`
- 报价相关参考: `usage_quote.ipynb`

## 韭菜下单操作说明
具体操作方法参考wiki: [韭菜下单操作说明](https://github.com/LeekQuant/leekquant/wiki/%E9%9F%AD%E8%8F%9C%E4%B8%8B%E5%8D%95%E6%93%8D%E4%BD%9C%E8%AF%B4%E6%98%8E)<br>
![运行界面](https://github.com/LeekQuant/leekquant/blob/main/assets/images/guide1.png?raw=true)<br>
如无法满足您的需求，需要支持多用户以及其他高级功能等，可以联系作者定制

### 实例化Trader
自行查找本机的ip地址，windows下使用命令`ipconfig /all`查看, 本机也可以直接用`localhost`或`127.0.0.1`

```python
ip = '127.0.0.1' #以机器实际IP为准, 本机可以是localhost或127.0.0.1
mark = 3721 # 标识列
trader = ThsTrader(ip, mark)
```

### 查询持仓
```python
df = trader.get_position(to_dataframe=True)
```
* `to_dataframe`用来控制返回的结果是否以`pd.DataFrame`形式返回，否则是`dict`格式

### 查询资金账户
```python
d = trader.get_balance()
```
* 返回`dict`

### 查询今日成交
```python
df = trader.get_today_trades(to_dataframe=True)
```
* 指定`to_dataframe=True`则返回`pd.DataFrame`

### 查询今日委托
```python
df = trader.get_today_entrusts(to_dataframe=True)
```
* 指定`to_dataframe=True`则返回`pd.DataFrame`

### 买入
```python
res = trader.buy(code, price, num)
```
* 参数说明:
  * 第一位`code`必须是6位字符串, 
  * 第二位`price`价格, 必须是浮点数, 具体是2位小数还是3为小数，依据下单的标的决定
  * 第三位`num`是数量, 股票以100为单位，可转债以10为单位
  * 示例: `trader.buy('513330', 0.311, 100)`
* 返回值`res`: 买入成功则会返回成交的合同号, 买入失败则会返回完整的出错信息 (依赖下单程序的弹窗)
 
### 卖出
```python
res = trader.sell('513330', 1.11, 100)
```
* 参数和返回值和`买入`一样

### 撤单
撤单目前不支持撤具体某笔单子，支持`撤所有买`, `撤所有卖` 和 `撤所有`，分别对应: `buy`, `sell`, `all`三个参数

```python
# 撤买
res = trader.cancel('buy')
# 撤卖
res = trader.cancel('sell')
# 撤所有
res = trader.cancel('all')
```
* 返回值`res`: 返回具体的撤单结果 (依赖下单程序的弹窗)

## 问财
`WenCai.query()`支持3个参数`question:str`, `columns:list`, `limit:int`
- 参数`question`: 字符串, 问财的问题语句,使用英分号;分割, 例如:非st;主板;非退市;行业;今日竞价涨幅小于3%;
- 参数`columns`: 数组, 显示的额外列，默认只显示股票简称和股票代码, 具体列名参考问财网站, 列名是包含关系
- 参数`limit`: 整数, 控制返回的条数，默认100条，最大100条

### 示例
```python
from leekquant.ths_wencai import WenCai
WenCai.query(question='非st;主板;非退市;行业;今日竞价涨幅小于3%;dde连3日飘红;', columns=['dde','涨幅'], limit=5)
```
详细用法参考`usage_wencai.ipynb`

## 报价

### level1报价订阅
支持level1实盘报价, 具体用法参考 `usage_quote.ipynb` 或者直接运行 `leekquant`目录下的`quote.py`文件

```python
from leekquant.quote import Quote

# 初始化
q = Quote()

# 定义一个回调, 所有收到的tick都在这里
def tick_handler(tick):
    print(tick)

# 注册回调
q.reg_tick_handler(tick_handler)

# 订阅你感兴趣的标的, 有任何tick数据，都会推送到回调函数里
# 最多订阅20只，订阅多了不会报错，也不会推送任何数据
q.sub_tick(codes=['603690.SH','002371.SZ','300812.SZ','300604.SZ','003043.SZ'])
```

### 全市场概况订阅
全市场订阅返回的数据包括：大盘(沪深创业板), 上涨下跌概况，张跌停概况，北向资金概况
```python
def overview_handler(data):
    print('收到市场概况:', data)
q.reg_overview_handler(overview_handler)
q.sub_overview()
```

## 支持券商
* 理论上只要券商支持同花顺下单都可以支持
* 下单主程序`xiadan.exe`要求最新通用版本`5.19.*`版

## 技术原理
* 和其他几个开源的键盘鼠标模拟(例如`pywinauto`)类似，都是从底部驱动键盘和鼠标操作
* 需要单独下载辅助程序`韭菜下单.exe`

## 常见问题
* 为什么无法连接？
  - 首先检查`xiadan.exe`的版本，必须是最新的下单通用版，去同花顺官网下载最新的
  - 执行顺序必须按照`先运行韭菜下单`, 然后`选择xiadan.exe`，点击`执行`的顺序，不可改动
  - 确认`xiadan.exe`是否掉线了，长时间不在线容易被踢下线，需要手动随便点击一下就激活连接
  - 如果windows有防火墙提示，则允许访问

## 后续工作
* 股票、转债、指数等的实时报价推送
* 同花顺热点的实时推送
* 其他语言支持
* 简单量化框架，着眼于实盘

## 联系作者
有问题可以联系作者:`leek.quant@gmail.com`, 也可以直接提issue或者发PR