import json
from database.db import get_connection

def create_incident(metric,value,severity,message,root_cause=None,recommendations=None):
    c=get_connection()
    cur=c.cursor()
    cur.execute("""INSERT INTO incidents
    (incident_number,metric,value,severity,message,root_cause,recommendations)
    VALUES (?,?,?,?,?,?,?)""",
    ("TEMP",metric,value,severity,message,json.dumps(root_cause or []),json.dumps(recommendations or [])))
    iid=cur.lastrowid
    number=f"INC-{iid:04d}"
    cur.execute("UPDATE incidents SET incident_number=? WHERE id=?",(number,iid))
    c.commit(); c.close()
    return number

def decode(row):
    if not row: return None
    d=dict(row)
    for k in ("root_cause","recommendations"):
        try: d[k]=json.loads(d[k] or "[]")
        except Exception: d[k]=[]
    d["verified"]=bool(d["verified"])
    return d

def get_incidents():
    c=get_connection()
    rows=c.execute("SELECT * FROM incidents ORDER BY id DESC").fetchall()
    out=[decode(r) for r in rows]
    c.close(); return out

def get_incident(iid):
    c=get_connection()
    row=c.execute("SELECT * FROM incidents WHERE id=?",(iid,)).fetchone()
    c.close(); return decode(row)

def update_incident(iid,status):
    allowed={"OPEN","INVESTIGATING","APPROVED","RESOLVED","CLOSED"}
    status=status.upper()
    if status not in allowed: return {"error":f"Invalid status: {sorted(allowed)}"}
    c=get_connection()
    cur=c.execute("UPDATE incidents SET status=?,updated_at=CURRENT_TIMESTAMP WHERE id=?",(status,iid))
    c.commit(); c.close()
    return {"updated":cur.rowcount,"incident_id":iid,"status":status}
