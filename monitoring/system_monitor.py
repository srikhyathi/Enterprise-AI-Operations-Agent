import psutil

def get_system_metrics():
    partitions = psutil.disk_partitions()
    root = partitions[0].mountpoint if partitions else "/"
    mem = psutil.virtual_memory()
    disk = psutil.disk_usage(root)
    return {
        "cpu_usage_percent": psutil.cpu_percent(interval=0.5),
        "memory_usage_percent": mem.percent,
        "memory_total_gb": round(mem.total / (1024**3), 2),
        "memory_available_gb": round(mem.available / (1024**3), 2),
        "disk_usage_percent": disk.percent,
        "disk_total_gb": round(disk.total / (1024**3), 2),
        "disk_free_gb": round(disk.free / (1024**3), 2)
    }
