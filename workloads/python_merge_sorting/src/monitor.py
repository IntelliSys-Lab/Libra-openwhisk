import time

clockTicksPerSecond  = 100
nanoSecondsPerSecond = 1e9
megabytesPerByte = 1e6


def monitor_peak(interval, queue_cpu, queue_mem, stop_signal=None):
    
    while not stop_signal.is_set():
    # while True:
        # CPU percentage
        prev_cpu_usage = int(open('/sys/fs/cgroup/cpu.stat', 'r').readlines()[0].split()[-1]) * 1000  # Convert from microseconds to nanoseconds
        prev_system_usage = 0
        prev_system_cpu_times = open('/proc/stat', 'r').readline().split()

        for i in range(1, 9):
            prev_system_usage = prev_system_usage + int(prev_system_cpu_times[i])

        time.sleep(interval) 
        
        after_cpu_usage = int(open('/sys/fs/cgroup/cpu.stat', 'r').readlines()[0].split()[-1]) * 1000  # Convert from microseconds to nanoseconds
        after_system_usage = 0
        after_system_cpu_times = open('/proc/stat', 'r').readline().split()

        cpu_timestamp = time.time()

        for i in range(1, 9):
            after_system_usage = after_system_usage + int(after_system_cpu_times[i])

        delta_cpu_usage = after_cpu_usage - prev_cpu_usage
        delta_system_usage = (after_system_usage - prev_system_usage) * nanoSecondsPerSecond / clockTicksPerSecond

        # Assuming the cgroup is allowed to use all CPUs, otherwise, you need to calculate online_cpus based on cgroup settings
        online_cpus = len(prev_system_cpu_times) - 1

        cpu_core_busy = delta_cpu_usage / delta_system_usage * online_cpus

        # Memory percentage
        mem_total = int(open('/sys/fs/cgroup/memory.current', 'r').read())
        mem_stat_lines = open('/sys/fs/cgroup/memory.stat', 'r').readlines()
        mem_cache = int([line for line in mem_stat_lines if 'file' in line][0].split()[-1])  # 'file' indicates the memory used by the cache

        mem_timestamp = time.time()

        mem_mb_busy = (mem_total - mem_cache) / megabytesPerByte
        
        queue_cpu.put((cpu_timestamp, cpu_core_busy))
        queue_mem.put((mem_timestamp, mem_mb_busy))
        

# if __name__ == "__main__":
#     monitor_peak(0.1, Queue(), Queue())