import os
from taskslist import UPLOAD,TRANSCODE


RecorderPath = '.\BililiveRecorder\BililiveRecorder.Cli.exe'
api_port = 8200
sendHeartBeat = True

works_path = "F:\\录播"
out_path = "./out"

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
