import psutil
def cpu():
    cpu = psutil.cpu_count()
    cpu_logical = psutil.cpu_count(logical=False)
    cpu_per = psutil.cpu_percent(1)
    cpuinfo = {
        'cpu': cpu,
        'cpu_logical': cpu_logical,
        'percent': cpu_per
    }
    return cpuinfo
# 监控内存信息：.
def mem():
#	mem = psutil.virtual_memory()   查看内存信息；
	mem_total = psutil.virtual_memory()[0]/1024/1024/1024
	mem_used = psutil.virtual_memory()[3] / 1024 / 1024/1024
	mem_per = psutil.virtual_memory()[2]
	mem_info = {
		'total': mem_total,
		'used': mem_used,
		'percent': mem_per
	}
	return mem_info
# 监控硬盘使用率：
def disk():
    total = psutil.disk_usage('F:\\录播')[0] / 1024 / 1024/1024
    used = psutil.disk_usage('F:\\录播')[1] / 1024 / 1024 / 1024
    free = psutil.disk_usage('F:\\录播')[2] / 1024 / 1024 / 1024
    percent = psutil.disk_usage('F:\\录播')[3]
    diskinfo = {
        'total':total,
        'used':used,
        'free':free,
        'percent':percent
    }
    return diskinfo
def network ():
#	network = psutil.net_io_counters() #查看网络流量的信息；
	network_sent = psutil.net_io_counters()[0]/8/1024 #每秒接受的kb
	network_recv = psutil.net_io_counters()[1]/8/1024
	network_info = {
		'network_sent' : network_sent,
		'network_recv' : network_recv
	}
	return network_info

def infolist():
    res = {"UUID":"ca4d9c3f-a5fe-4eb8-a8b2-43da82f94c9c","name":"NGlive-1","cpu":cpu(),"memory":mem(),"disk":disk()}
    return res

    
def get_sys_info(ws):
    import time,json
    from log import logger
    def send(message,ws):
        try:
            ws.send(json.dumps(message))
        except:
            logger.warning('ws推送失败，请检查网络连接')
    while True:
        time.sleep(5)
        send(infolist(),ws)
