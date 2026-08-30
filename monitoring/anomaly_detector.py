CPU_WARNING, CPU_CRITICAL = 70, 90
MEMORY_WARNING, MEMORY_CRITICAL = 75, 90
DISK_WARNING, DISK_CRITICAL = 80, 90

def detect_anomalies(metrics):
    alerts = []
    checks = [
        ("CPU", metrics["cpu_usage_percent"], CPU_WARNING, CPU_CRITICAL, "CPU usage is high.", "CPU usage is critically high."),
        ("Memory", metrics["memory_usage_percent"], MEMORY_WARNING, MEMORY_CRITICAL, "Memory usage is high.", "Memory usage is critically high."),
        ("Disk", metrics["disk_usage_percent"], DISK_WARNING, DISK_CRITICAL, "Disk usage is high.", "Disk usage is critically high."),
    ]
    for metric, value, warning, critical, wmsg, cmsg in checks:
        if value >= critical:
            alerts.append({"metric": metric, "value": value, "severity": "CRITICAL", "message": cmsg})
        elif value >= warning:
            alerts.append({"metric": metric, "value": value, "severity": "WARNING", "message": wmsg})
    return alerts
