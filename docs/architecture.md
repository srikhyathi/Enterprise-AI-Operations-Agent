# Architecture

System/application evidence is collected by monitoring and log-analysis components. The Operations Agent correlates the evidence and either uses an optional OpenAI-compatible LLM or a deterministic fallback. Incidents are persisted in SQLite. The workflow supports approval, safe remediation simulation and verification. FastAPI exposes APIs and a browser dashboard consumes them.

## Production safety

The included remediation is intentionally non-destructive and simulated. Production actions should use an allowlist, RBAC, approval, audit logs, timeouts, rollback and least-privilege credentials. The Kubernetes and Docker files are deployment starters and require environment-specific secrets/image registries.
