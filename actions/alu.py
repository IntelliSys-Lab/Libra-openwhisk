import datetime
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__))))
import json
import time
import os
import random
from multiprocessing import Process, Pipe
from threading import Thread
from queue import Queue

# !pip install couchdb
# import couchdb
# from monitor import monitor_peak


import time

clockTicksPerSecond  = 100
nanoSecondsPerSecond = 1e9
megabytesPerByte = 1e6


def monitor_peak(interval, queue_cpu, queue_mem):
    
    while True:
        # CPU percentage
        prev_cpu_usage = 0
        prev_system_usage = 0
        prev_cgroup_cpu_times = open('/sys/fs/cgroup/cpuacct/cpuacct.usage_percpu', 'r').readline().split()
        prev_system_cpu_times = open('/proc/stat', 'r').readline().split()

        for per_cpu in prev_cgroup_cpu_times:
            prev_cpu_usage = prev_cpu_usage + int(per_cpu)
        for i in range(1, 9):
            prev_system_usage = prev_system_usage + int(prev_system_cpu_times[i])

        time.sleep(interval) 
        
        after_cpu_usage = 0
        after_system_usage = 0
        after_cgroup_cpu_times = open('/sys/fs/cgroup/cpuacct/cpuacct.usage_percpu', 'r').readline().split()
        after_system_cpu_times = open('/proc/stat', 'r').readline().split()

        cpu_timestamp = time.time()

        for per_cpu in after_cgroup_cpu_times:
            after_cpu_usage = after_cpu_usage + int(per_cpu)
        for i in range(1, 9):
            after_system_usage = after_system_usage + int(after_system_cpu_times[i])

        delta_cpu_usage = after_cpu_usage - prev_cpu_usage
        delta_system_usage = (after_system_usage - prev_system_usage) * nanoSecondsPerSecond / clockTicksPerSecond
        online_cpus = max(len(prev_cgroup_cpu_times), len(after_cgroup_cpu_times))

        cpu_core_busy = delta_cpu_usage / delta_system_usage * online_cpus

        # Memory percentage
        mem_total = int(open('/sys/fs/cgroup/memory/memory.usage_in_bytes', 'r').read())
        mem_cache = int(open('/sys/fs/cgroup/memory/memory.stat', 'r').readlines()[-3].split()[-1])

        mem_timestamp = time.time()

        mem_mb_busy = (mem_total - mem_cache) / megabytesPerByte
        
        queue_cpu.put((cpu_timestamp, cpu_core_busy))
        queue_mem.put((mem_timestamp, mem_mb_busy))
        


interval = 0.02

# def upload_stream_to_couchdb(db, doc_id, content, filename, content_type=None):
#     try:
#         db.put_attachment(
#             doc=db[doc_id],
#             content=content,
#             filename=filename,
#             content_type=content_type
#         )
#     except couchdb.http.ResourceConflict:
#         pass

def alu(per_size, childConn, clientId):
    a = random.randint(100, 10000)
    b = random.randint(100, 10000)
    temp = 0
    for i in range(per_size):
        if i % 4 == 0:
            temp = a + b
        elif i % 4 == 1:
            temp = a - b
        elif i % 4 == 2:
            temp = a * b
        else:
            temp = a / b

    childConn.send("Calulation {} result {}".format(clientId, temp))
    childConn.close()

def handler(event):
    context = None
    q_cpu = Queue()
    q_mem = Queue()
    t = Thread(
        target=monitor_peak,
        args=(interval, q_cpu, q_mem),
        daemon=True
    )
    t.start()

    size = event.get('size')
    parallel = event.get('parallel')
    couch_link = event.get('couch_link')
    db_name = event.get('db_name')

    # couch = couchdb.Server(couch_link)
    # db = couch[db_name]

    process_begin = datetime.datetime.now()
    per_size = int(size/parallel)
    tail_size = size % parallel
    childConns = []
    parentConns = []
    jobs = []
    for i in range(parallel+1):
        parentConn, childConn = Pipe()
        parentConns.append(parentConn)
        childConns.append(childConn)
        if i == parallel:
            p = Process(target=alu, args=(tail_size, childConn, i))
        else:
            p = Process(target=alu, args=(per_size, childConn, i))
        jobs.append(p)
    for p in jobs:
        p.start()
    for p in jobs:
        p.join()
    
    results = []
    for con in parentConns:
        results.append(con.recv())

    # upload_stream_to_couchdb(db, "result", '\n'.join(results).encode("utf-8"), "result.txt")
    process_end = datetime.datetime.now()
    process_time = (process_end - process_begin) / datetime.timedelta(microseconds=1)

    cpu_timestamp = []
    cpu_usage = []
    while q_cpu.empty() is False:
        (timestamp, cpu) = q_cpu.get()
        cpu_timestamp.append(timestamp)
        cpu_usage.append(cpu)

    mem_timestamp = []
    mem_usage = []
    while q_mem.empty() is False:
        (timestamp, mem) = q_mem.get()
        mem_timestamp.append(timestamp)
        mem_usage.append(mem)

    return {
        "cpu_timestamp": [str(x) for x in cpu_timestamp],
        "cpu_usage": [str(x) for x in cpu_usage],
        "mem_timestamp": [str(x) for x in mem_timestamp],
        "mem_usage": [str(x) for x in mem_usage]
    }
    
def main(dict):
	return handler(dict)