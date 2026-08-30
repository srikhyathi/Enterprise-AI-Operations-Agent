# API

GET /health
GET /metrics
GET /metrics/prometheus
GET /anomalies
GET /logs
GET /ai/analyze
GET /ai/root-cause
GET /incidents
GET /incidents/{id}
POST /incidents/create
POST /incidents/{id}/approve
PATCH /incidents/{id}?status=...
POST /incidents/{id}/remediate
POST /incidents/{id}/verify
