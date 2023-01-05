## SLOGAN
让韭菜的股票量化变得更加简单

## 缘起
* 目前韭菜的量化门槛太高，虽然有很多很好的量化平台，但是要么门槛高，要么手续费高
* 开源的几个THS下单都有各种各样的问题，维护都不是很及时
* 受益于此项目[thsauto](https://github.com/match5/thsauto)启发，实现一个类似的`REST`接口，方便各种语言接入

## 项目功能
* 进行自动的程序化股票交易
* 支持同花顺最新版通用下单程序(同花顺官网下载最新版里面带的xiadan.exe)
* 支持通过`webserver`远程操作客户端
* 支持标准Rest接口调用，方便其他语言适配
* 本项目是基于Rest标准接口的Python3.7实现

## REST接口
查询持仓  
> curl -H "Content-Type: application/json" -X POST http://localhost:3721/api/get_position -d "{}"

查询资金账户
> curl -H "Content-Type: application/json" -X POST http://localhost:3721/api/get_balance -d "{}"

查询今日成交
> curl -H "Content-Type: application/json" -X POST http://localhost:3721/api/get_today_trades -d "{}"

查询今日委托 
> curl -H "Content-Type: application/json" -X POST http://localhost:3721/api/get_today_entrusts -d "{}"

买入贵州茅台100股,价格1700.0元
> curl -H "Content-Type: application/json" -X POST http://localhost:3721/api/buy -d '["600519", 1700.0, 100]'

卖出贵州茅台100股,价格1800.0元
> curl -H "Content-Type: application/json" -X POST http://localhost:3721/api/sell -d '["600519",1800.0,100]'

撤所有买单(`buy`), 撤所有卖单(`sell`), 撤所有(`all`)
> curl -H "Content-Type: application/json" -X POST http://localhost:3721/api/cancel_entrust -d '[buy|sell|all]'

## 运行项目
### **创建虚拟环境**
> conda create -n leekquant python=3.7
### 激活虚拟环境
> conda activate leekquant
### 安装依赖
> pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple/
### 用法参考测试用例
`test.py`里面有各种操作的实现

## 具体操作说明
**注意事项：**
* 使用前请务必注意：`韭菜下单`目前只是个测试版本，没有任何安全鉴权，只可用在可信任的局域网内，切记！
* 请将同花顺下单软件里的`撤单前是否需要确认`和`委托前是否需要确认`设置为`否`,  具体设置是在`系统设置`=>`快速交易`里更改
* 如果需要错误信息，则下单程序要打开弹框，如果不需要可以关掉弹框，下单买卖速度更快
* 请关闭`360`或者`电脑管家`等安全软件，或者设置信任韭菜下单程序

### 运行韭菜下单
`韭菜下单`是同花顺下单程序和ThsTrader之间的代理Proxy，负责转发指令，以及提供webservice等相关REST服务, 目前免费测试中。
1. 运行`assets/xiadan`目录下的`韭菜下单.exe`, 选择同花顺下单程序`xiadan.exe`, 点击`执行`，拉起下单程序后，手工输入账号密码登录。 (必须按此步骤，不可变更)
2. 记录`韭菜下单`页面的`标识`，后续程序需要
3. 自行查找本机的ip地址，windows下使用命令`ipconfig /all`查看, 本机也可以直接用`localhost`

如无法满足您的需求，需要支持多用户以及其他高级功能等，可以联系作者定制

### 实例化Trader
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
* 返回`dict`格式的结果

### 查询今日成交
```python
df = trader.get_today_trades(to_dataframe=True)
if not df.empty:
    log.debug('\n{}', tabulate(df, headers='keys', tablefmt='psql'))
else:
    log.debug('无今日成交')
```

### 查询今日委托
```python
df = trader.get_today_entrusts(to_dataframe=True)
if not df.empty:
    log.debug('\n{}', tabulate(df, headers='keys', tablefmt='psql'))
else:
    log.debug('无今日委托')
```

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