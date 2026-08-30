from database.db import get_connection
from monitoring.system_monitor import get_system_metrics
from monitoring.anomaly_detector import detect_anomalies
from remediation.incident_manager import get_incident

def verify_incident(incident_id):
    item=get_incident(incident_id)
    if not item: return {"error":"Incident not found"}
    metrics=get_system_metrics()
    alerts=detect_anomalies(metrics)
    passed=len(alerts)==0
    c=get_connection()
    c.execute("""UPDATE incidents SET verified=?,status=?,updated_at=CURRENT_TIMESTAMP WHERE id=?""",
              (1 if passed else 0,"RESOLVED" if passed else "INVESTIGATING",incident_id))
    c.commit(); c.close()
    return {"incident_id":incident_id,"verification":"PASSED" if passed else "FAILED",
            "current_metrics":metrics,"current_alerts":alerts}
