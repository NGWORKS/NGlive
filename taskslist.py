"""
任务队列
"""
from collections import deque
import pickle,os


# 转码队列
TRANSCODE = deque()
# 上传队列
UPLOAD = deque()

def Save_list():
    if len(TRANSCODE) != 0:
        TR = pickle.dumps(TRANSCODE)
        with open('Transcode.tmp','wb') as f:
            f.write(TR)
            f.close()
    
    if len(UPLOAD) != 0:
        TR = pickle.dumps(UPLOAD)
        with open('Upload.tmp','wb') as f:
            f.write(TR)
            f.close()

def Load_list():
    global TRANSCODE,UPLOAD
    if os.path.isfile("Transcode.tmp"):
        f=open("Transcode.tmp","rb")
        TRANSCODE = pickle.load(f)
        f.close()
        os.remove("Transcode.tmp")
    
    if os.path.isfile("Upload.tmp"):
        f=open("Upload.tmp","rb")
        UPLOAD = pickle.load(f)
        f.close()
        os.remove("Upload.tmp")

if __name__ == "__main__":
    TRANSCODE.append(1)
    UPLOAD.append(2)
    Save_list()
    import time
    time.sleep(5)
    Load_list()
    print(TRANSCODE.pop())
    print(UPLOAD.pop())


    

