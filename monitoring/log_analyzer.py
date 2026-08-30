from pathlib import Path
import re

LOG_FILE = Path(__file__).resolve().parent.parent / "logs" / "application.log"

def analyze_logs():
    errors, warnings, info = [], [], []
    if LOG_FILE.exists():
        for line in LOG_FILE.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if re.search(r"\sERROR\s", line):
                errors.append(line)
            elif re.search(r"\sWARNING\s", line):
                warnings.append(line)
            elif re.search(r"\sINFO\s", line):
                info.append(line)
    return {
        "total_errors": len(errors), "total_warnings": len(warnings),
        "errors": errors, "warnings": warnings, "info_count": len(info)
    }
