# 高度自动化的录播服务端！
这里应该有图 但是还没有做
## 一、项目介绍

### 1、介绍

这是NGlive的录播服务器集群的客户端部分实现代码，它可以自动化的进行录制-压制-上传-通知，同时流程高度可自定义，并且可以任意受中心服务器的调度，有一定的错误修复能力。可以保证长期稳定的运行。


### 2、基本功能
这个客户端集 录制、转码压制、上传为一体，同时集成了正向反向API、WS等功能
如下图所示：
这里应该有图、但是还没有做


### 3、环境
本项目基于**Python3.9.0**开发，**在其他版本的运行状态未知**。**请在安装依赖前阅读下面的说明** 可以有效减少出问题的概率。

### 4、依赖
|  Package  |  Version  |
|-----------|   ------  |
|baidupcs-py|    0.6.25 |
|requests   |    2.26.0 |
|fastapi    |    0.63.0 |
|pydantic   |    1.7.3  |
|pathlib    |    1.0.1  |
|SQLAlchemy |    1.3.22 |
|loguru     |    0.5.3  |
|websockets |    8.1    |

* 安装 `baidupcs-py` 时，请前往 [这里](https://github.com/PeterDing/BaiduPCS-Py) **仔细阅读安装注意事项**

### 5、项目结构
本项目结构如下：
```
├─ BililiveRecorder  录播姬
|  __GraphQL.py      封装了部分graphql方法
│  README.md         自述文件
│  LICENSE           LICENSE
│  db.py             数据库的定义和基本操作   
|  eventManager.py   事件驱动核心 
|  eventRun.py       NGlive任务管理
|  initial.py        配置文件
|  linstener.py      监听-响应模块
|  log.py            日志配置
|  orm.py            验证-整理数据
|  resquest_test.py  验证-整理数据
|  systemInfo.py     系统监控
|  taskslist.py      任务队列
|  trcode.py         转码模块
|  up.py             上传模块
|  upload.py         上传功能的实现
|  wsclient.py       ws模块
|  api.py            程序入口

```
### 6、交流
外联群QQ:781665797

# 二、使用
## 配置录播姬
略 请参考 [`BililiveRecorder`](https://github.com/Bililive/BililiveRecorder)的配置文档
录播姬需要配置webhook

## 配置NGlive
下载本项目后，用任意IDE打开 `initial.py`

找到以下代码片段：
```python
# 录播姬位置 如果您没有使用webapi版本的录播姬会导致一些错误发送
RecorderPath = '.\BililiveRecorder\BililiveRecorder.Cli.exe'
# 录播姬 webapi启动端口
api_port = 8200
# 发送心跳包
sendHeartBeat = True

# 录播姬的工作目录
works_path = "F:\\录播"

# 转码输出位置
out_path = "./out"

# 录播姬需要配置 webhook 地址为 下面的ip和端口加上路径 /webhook/
# NGlive 正向服务器地址
NGhost = "127.0.0.1"

# NGlive 服务器端口
NGport = "8100"
```
根据自己的实际情况配置。

## 直接使用
您仅需要按照上述方法配置后下载本项目，双击运行`api.py`文件。

## 终端中运行
您可以在项目目录下打开终端：
输入以下命令：

```
python api.py
```


# 三、如何工作
TODO

# 四、贡献 - 特别感谢 - license
## 1、贡献
如果您发现了更好的使用方法，不妨分享出来！你可以使用pr功能提交请求，我会审阅。或者在使用中出现了什么问题，都可以提交issue，或者加入我们的`外联群（QQ:781665797）`交流。

## 2、特别感谢
- [`baidupcs-py`](https://github.com/PeterDing/BaiduPCS-Py)：非常详细的百度网盘api库
- [`BililiveRecorder`](https://github.com/Bililive/BililiveRecorder)：强大的录播姬
- [`fastapi`](https://github.com/tiangolo/fastapi)：快速且高性能的 web 框架
## 3、license
[`GNU AGPLv3`](https://choosealicense.com/licenses/agpl-3.0/) 许可证
