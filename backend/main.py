import os
from datetime import datetime, timezone
from typing import Optional

from fastapi import FastAPI, HTTPException, Header, Query
from fastapi.responses import FileResponse, PlainTextResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

from database.db import initialize_database
from monitoring.system_monitor import get_system_metrics
from monitoring.anomaly_detector import detect_anomalies
from monitoring.log_analyzer import analyze_logs
from monitoring.prometheus_exporter import prometheus_text
from ai_agent.operations_agent import analyze_operations
from remediation.incident_manager import (
    create_incident, get_incidents, get_incident, update_incident,
)
from remediation.remediation_engine import execute_remediation
from remediation.verification import verify_incident

app = FastAPI(
    title="Enterprise AI Operations Agent",
    version="3.0.0",
    description="Complete portfolio-grade software-only AIOps platform."
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], allow_credentials=True,
    allow_methods=["*"], allow_headers=["*"],
)

initialize_database()
FRONTEND_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "frontend")
app.mount("/static", StaticFiles(directory=FRONTEND_DIR), name="static")

API_KEY = os.getenv("OPS_API_KEY", "")

def authorize(x_api_key: Optional[str]):
    if API_KEY and x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API key")

@app.get("/", include_in_schema=False)
def home():
    return FileResponse(os.path.join(FRONTEND_DIR, "index.html"))

@app.get("/health")
def health():
    return {"status": "healthy", "timestamp": datetime.now(timezone.utc).isoformat()}

@app.get("/metrics")
def metrics():
    return get_system_metrics()

@app.get("/metrics/prometheus", response_class=PlainTextResponse)
def metrics_prometheus():
    return prometheus_text(get_system_metrics())

@app.get("/anomalies")
def anomalies():
    m = get_system_metrics()
    alerts = detect_anomalies(m)
    return {"metrics": m, "status": "HEALTHY" if not alerts else "ISSUES_DETECTED", "alerts": alerts}

@app.get("/logs")
def logs():
    return analyze_logs()

@app.get("/ai/analyze")
def ai_analysis():
    return analyze_operations()

@app.get("/ai/root-cause")
def root_cause():
    result = analyze_operations()
    return {
        "root_cause_analysis": result["root_cause_analysis"],
        "analysis_mode": result["analysis_mode"]
    }

@app.post("/incidents/create")
def create_detected_incidents(x_api_key: Optional[str] = Header(default=None)):
    authorize(x_api_key)
    result = analyze_operations()
    created = []
    rca = result["root_cause_analysis"]

    for alert in result["system_alerts"]:
        created.append(create_incident(
            metric=alert["metric"], value=alert["value"],
            severity=alert["severity"], message=alert["message"],
            root_cause=rca["findings"], recommendations=rca["recommendations"]
        ))

    logs = result["log_analysis"]
    if logs["total_errors"]:
        created.append(create_incident(
            metric="APPLICATION_LOG", value=logs["total_errors"],
            severity="CRITICAL" if logs["total_errors"] >= 5 else "HIGH",
            message=f"Application log contains {logs['total_errors']} error(s).",
            root_cause=rca["findings"], recommendations=rca["recommendations"]
        ))
    return {"created_incidents": created, "count": len(created)}

@app.get("/incidents")
def incidents():
    return {"incidents": get_incidents()}

@app.get("/incidents/{incident_id}")
def incident(incident_id: int):
    item = get_incident(incident_id)
    if not item:
        raise HTTPException(status_code=404, detail="Incident not found")
    return item

@app.patch("/incidents/{incident_id}")
def change_incident_status(
    incident_id: int,
    status: str = Query(...),
    x_api_key: Optional[str] = Header(default=None)
):
    authorize(x_api_key)
    result = update_incident(incident_id, status)
    if result.get("updated") == 0:
        raise HTTPException(status_code=404, detail="Incident not found")
    return result

@app.post("/incidents/{incident_id}/approve")
def approve_incident(incident_id: int, x_api_key: Optional[str] = Header(default=None)):
    authorize(x_api_key)
    item = get_incident(incident_id)
    if not item:
        raise HTTPException(status_code=404, detail="Incident not found")
    result = update_incident(incident_id, "APPROVED")
    return result

@app.post("/incidents/{incident_id}/remediate")
def remediate(incident_id: int, x_api_key: Optional[str] = Header(default=None)):
    authorize(x_api_key)
    item = get_incident(incident_id)
    if not item:
        raise HTTPException(status_code=404, detail="Incident not found")
    if item["status"] != "APPROVED":
        raise HTTPException(status_code=400, detail="Incident requires APPROVED status before remediation.")
    return execute_remediation(incident_id)

@app.post("/incidents/{incident_id}/verify")
def verify(incident_id: int, x_api_key: Optional[str] = Header(default=None)):
    authorize(x_api_key)
    if not get_incident(incident_id):
        raise HTTPException(status_code=404, detail="Incident not found")
    return verify_incident(incident_id)
