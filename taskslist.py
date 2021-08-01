"""
任务队列
"""
from queue import Queue
import pickle,os


# 转码队列
TRANSCODE = Queue()
# 上传队列
UPLOAD = Queue()

def Save_list():
    if not TRANSCODE.empty():
        i = 0
        tclist = []
        while i <= TRANSCODE.qsize():
            tclist.append(TRANSCODE.get())
            i+=1
            
        TR = pickle.dumps(tclist)
        with open('Transcode.tmp','wb') as f:
            f.write(TR)
            f.close()
    
    if not UPLOAD.empty():
        i = 0
        tclist = []
        while i <= UPLOAD.qsize():
            tclist.append(UPLOAD.get())
            i+=1
        TR = pickle.dumps(tclist)
        with open('Upload.tmp','wb') as f:
            f.write(TR)
            f.close()

def Load_list():
    if os.path.isfile("Transcode.tmp"):
        f=open("Transcode.tmp","rb")
        tclist = pickle.load(f)
        for element in tclist:
            TRANSCODE.put(element)
        f.close()
        os.remove("Transcode.tmp")
    
    if os.path.isfile("Upload.tmp"):
        f=open("Upload.tmp","rb")
        tclist = pickle.load(f)
        for element in tclist:
            UPLOAD.put(element)
        f.close()
        os.remove("Upload.tmp")

if __name__ == "__main__":
    TRANSCODE.put(1)
    UPLOAD.put(2)
    Save_list()
    import time
    time.sleep(5)
    Load_list()
    print(TRANSCODE.get())
    print(UPLOAD.get())


    

