from fastapi.testclient import TestClient
from backend.main import app

client=TestClient(app)

def test_health():
    r=client.get("/health"); assert r.status_code==200; assert r.json()["status"]=="healthy"
def test_metrics():
    r=client.get("/metrics"); assert r.status_code==200; assert "cpu_usage_percent" in r.json()
def test_prometheus():
    r=client.get("/metrics/prometheus"); assert r.status_code==200; assert "ops_cpu_usage_percent" in r.text
def test_logs():
    r=client.get("/logs"); assert r.status_code==200; assert r.json()["total_errors"]>=3
def test_ai():
    r=client.get("/ai/analyze"); assert r.status_code==200; assert "root_cause_analysis" in r.json()
def test_incidents():
    r=client.get("/incidents"); assert r.status_code==200; assert "incidents" in r.json()
