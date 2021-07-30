"""
这个文件实现了对于NGlive一些简单的配置。
"""
import os
from taskslist import UPLOAD,TRANSCODE


# 录播姬位置
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



workpath = os.getcwd()
os.chdir(workpath)

if os.path.isabs(works_path):
    works_path = works_path
else:
    works_path = os.path.abspath(works_path)

if os.path.isabs(out_path):
    out_path = out_path
else:
    out_path = os.path.abspath(out_path)

if not os.path.isdir(out_path):
            os.makedirs(out_path)



"""
我们为您提供了控制录制流程的开放能力
您可以通过修改下列的变量，以达到对于录制流程控制的能力
"""
first_factory = [TRANSCODE]
second_factory = [("After_Transcode",UPLOAD)]
