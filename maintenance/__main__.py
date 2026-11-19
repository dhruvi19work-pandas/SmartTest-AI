import json
from maintenance.health_analyzer import HealingHealthAnalyzer
if __name__ == '__main__': print(json.dumps(HealingHealthAnalyzer().analyze(), indent=2))
