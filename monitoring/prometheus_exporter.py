def prometheus_text(metrics):
    return "\n".join([
        "# HELP ops_cpu_usage_percent Current CPU utilization.",
        "# TYPE ops_cpu_usage_percent gauge",
        f"ops_cpu_usage_percent {metrics['cpu_usage_percent']}",
        "# HELP ops_memory_usage_percent Current memory utilization.",
        "# TYPE ops_memory_usage_percent gauge",
        f"ops_memory_usage_percent {metrics['memory_usage_percent']}",
        "# HELP ops_disk_usage_percent Current disk utilization.",
        "# TYPE ops_disk_usage_percent gauge",
        f"ops_disk_usage_percent {metrics['disk_usage_percent']}",
    ]) + "\n"
