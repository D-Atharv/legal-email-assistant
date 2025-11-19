"""
Audit logging service.

Each analysis or drafting event can be stored as a JSON file
under static/audit_logs/ for traceability.

Runs asynchronously to avoid blocking requests.
"""



import json
import asyncio
from datetime import datetime
from pathlib import Path

from core.config import settings


# Ensure log directory exists
LOG_DIR = Path(settings.AUDIT_LOG_DIR)
LOG_DIR.mkdir(parents=True, exist_ok=True)


async def write_audit_log(entry: dict) -> None:
    """
    Save a single audit log entry to a JSON file.
    File naming format:
        audit-YYYYMMDD-HHMMSS-ms.json

    Args:
        entry (dict): The data to record (MCP tool calls, analysis results, drafts, etc.)
    """
    timestamp = datetime.utcnow().strftime("%Y%m%d-%H%M%S-%f")
    file_path = LOG_DIR / f"audit-{timestamp}.json"

    # Augment entry with timestamp for traceability
    entry_with_meta = {
        "timestamp": timestamp,
        "entry": entry,
    }

    # Async safe write
    loop = asyncio.get_event_loop()
    await loop.run_in_executor(None, _write_json, file_path, entry_with_meta)


def _write_json(path: Path, data: dict):
    """Blocking JSON write wrapped in async executor."""
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
