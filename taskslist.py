"""
任务队列
"""
from queue import Queue

# 转码队列
TRANSCODE = Queue(maxsize=0)
# 上传队列
UPLOAD = Queue(maxsize=0)