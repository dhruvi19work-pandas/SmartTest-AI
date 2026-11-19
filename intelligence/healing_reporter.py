
import json
from datetime import datetime, timezone
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parent.parent
REPORT_DIR = PROJECT_ROOT / "reports"

REPORT_DIR.mkdir(parents=True, exist_ok=True)


class HealingReporter:

    def __init__(self):
        self.report_file = REPORT_DIR / "healing_events.jsonl"

    def record_event(
        self,
        original_element,
        replacement_locator=None,
        confidence=0,
        status="FAILED",
        reason=""
    ):

        event = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "original_id": original_element.get("id"),
            "original_name": original_element.get("name"),
            "replacement_locator": replacement_locator,
            "confidence": confidence,
            "status": status,
            "reason": reason
        }

        with open(
            self.report_file,
            "a",
            encoding="utf-8"
        ) as file:

            file.write(
                json.dumps(event) + "\n"
            )
