# -*- coding: utf-8 -*-
"""
这个文件实现了对于NGlive一些简单的配置。
"""
import os
from taskslist import UPLOAD,TRANSCODE
from configparser import ConfigParser

config = ConfigParser()
config.read('config.ini',encoding="utf-8")


# 录播姬位置
RecorderPath = config['BASIC']['RecorderPath']
# 录播姬 webapi启动端口
api_port = config['BASIC']['api_port']

# 录播姬的工作目录
works_path = config['BASIC']['works_path']

# 转码输出位置
out_path = config['BASIC']['out_path']


# 录播姬需要配置 webhook 地址为 下面的ip和端口加上路径 /webhook/
# NGlive 正向服务器地址
NGhost = config['BASIC']['NGhost']

# NGlive 服务器端口
NGport = int(config['BASIC']['NGport'])

# ws
wspath =  config['BASIC']['wspath']
print(wspath)

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
