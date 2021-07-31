"""
任务队列
"""
from queue import Queue
from collections import deque
import pickle


# 转码队列
TRANSCODE = deque()
# 上传队列
UPLOAD = deque()