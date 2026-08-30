from database.db import get_connection
from remediation.incident_manager import get_incident

def execute_remediation(incident_id):
    item=get_incident(incident_id)
    if not item: return {"error":"Incident not found"}
    action="SAFE_DEMO_REMEDIATION: restart/cleanup action simulated; no OS command executed."
    c=get_connection()
    c.execute("""UPDATE incidents SET status='INVESTIGATING',
                 remediation_action=?, remediation_result=?,
                 updated_at=CURRENT_TIMESTAMP WHERE id=?""",
              (action,"Simulation completed successfully; verification required.",incident_id))
    c.commit(); c.close()
    return {"incident_id":incident_id,"status":"INVESTIGATING","action":action,
            "result":"Safe remediation simulation completed. Run verification."}
