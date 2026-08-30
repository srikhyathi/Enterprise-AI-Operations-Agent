import json, os, urllib.request
from monitoring.system_monitor import get_system_metrics
from monitoring.anomaly_detector import detect_anomalies
from monitoring.log_analyzer import analyze_logs

def rule_based_root_cause(metrics, alerts, logs):
    findings, recommendations = [], []
    errors, warnings = logs["errors"], logs["warnings"]
    db = any("database" in x.lower() for x in errors)
    payment = any("payment service" in x.lower() for x in errors)
    pool = any("connection pool" in x.lower() for x in warnings)
    if db and payment:
        findings.append("Database connectivity failure is likely causing the payment service failure.")
        recommendations.append("Check database availability and connection configuration.")
    if pool:
        findings.append("Database connection pool utilization is elevated.")
        recommendations.append("Investigate database connection usage and long-running queries.")
    if any("503" in x for x in errors):
        findings.append("A downstream service is returning HTTP 503, indicating temporary unavailability.")
        recommendations.append("Check service health, dependency availability and retry behavior.")
    for a in alerts:
        findings.append(f"{a['metric']} usage is {a['value']}% ({a['severity']}).")
    if not findings:
        findings.append("No significant root cause identified.")
    return {"findings": findings, "recommendations": recommendations}

def llm_root_cause(context):
    key = os.getenv("LLM_API_KEY") or os.getenv("OPENAI_API_KEY")
    if not key:
        return None
    base = os.getenv("LLM_BASE_URL", "https://api.openai.com/v1").rstrip("/")
    model = os.getenv("LLM_MODEL", "gpt-4o-mini")
    body = {
        "model": model,
        "messages": [
            {"role":"system","content":"You are an AIOps incident analyst. Return ONLY valid JSON with keys findings and recommendations. Use only supplied evidence; do not invent facts."},
            {"role":"user","content":json.dumps(context)}
        ],
        "temperature":0.1
    }
    req = urllib.request.Request(
        base + "/chat/completions",
        data=json.dumps(body).encode(),
        headers={"Content-Type":"application/json","Authorization":"Bearer "+key},
        method="POST"
    )
    try:
        with urllib.request.urlopen(req, timeout=20) as r:
            data=json.loads(r.read().decode())
        content=data["choices"][0]["message"]["content"]
        parsed=json.loads(content)
        if isinstance(parsed.get("findings"), list) and isinstance(parsed.get("recommendations"), list):
            return parsed
    except Exception:
        pass
    return None

def analyze_operations():
    metrics=get_system_metrics()
    alerts=detect_anomalies(metrics)
    logs=analyze_logs()
    context={"metrics":metrics,"alerts":alerts,"logs":logs}
    rules=rule_based_root_cause(metrics, alerts, logs)
    llm=llm_root_cause(context)
    return {
        "system_metrics":metrics,
        "system_alerts":alerts,
        "log_analysis":logs,
        "root_cause_analysis":llm or rules,
        "analysis_mode":"LLM" if llm else "RULE_BASED_FALLBACK"
    }
