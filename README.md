# Enterprise AI Operations Agent

A complete software-only AIOps portfolio project.

## Included

Monitoring, anomaly detection, application-log analysis, evidence correlation, optional LLM reasoning, root-cause analysis, incident lifecycle, approval workflow, safe remediation simulation, verification, web dashboard, API-key protection, Prometheus endpoint/config, Docker/Compose, Kubernetes starter, CI tests and documentation.

## Local Windows run

```cmd
C:\Users\Kailash\venv\Scripts\activate
pip install -r requirements.txt
uvicorn backend.main:app --reload
```

Open `http://127.0.0.1:8000`.

Swagger: `http://127.0.0.1:8000/docs`

## Demo

The included application log intentionally contains a simulated database/payment incident. In the dashboard click:

1. Create Incident
2. Approve
3. Run Safe Remediation
4. Verify

The remediation step is a safe simulation and does not execute arbitrary OS commands.

## LLM

Set `LLM_API_KEY` (or `OPENAI_API_KEY`) and optional `LLM_BASE_URL`/`LLM_MODEL`. Without a key, the project runs using its deterministic fallback.

## Docker

```cmd
docker compose up --build
```

Dashboard: `http://127.0.0.1:8000`
Prometheus: `http://127.0.0.1:9090`

## Tests

```cmd
pytest -q
```
