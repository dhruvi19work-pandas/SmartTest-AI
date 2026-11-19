import json
from collections import Counter
from pathlib import Path
from intelligence.healing_reporter import REPORT_DIR

class HealingHealthAnalyzer:
    def __init__(self, report_file=None): self.report_file=Path(report_file or REPORT_DIR/'healing_events.jsonl')
    def analyze(self):
        events=[]
        if self.report_file.exists():
            for line in self.report_file.read_text(encoding='utf-8').splitlines():
                try: events.append(json.loads(line))
                except json.JSONDecodeError: continue
        counts=Counter(e.get('status','UNKNOWN') for e in events)
        total=len(events); healed=counts.get('HEALED',0)
        return {'total_events':total,'status_counts':dict(counts),'healing_rate_percent':round(healed/total*100,2) if total else 0,
                'frequent_original_ids':Counter(e.get('original_id') or 'unknown' for e in events).most_common(10)}
