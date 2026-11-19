from test_generator.scenario_generator import ScenarioGenerator
from maintenance.health_analyzer import HealingHealthAnalyzer

def test_scenario_generator_creates_pytest_code():
    source=ScenarioGenerator().generate_login_tests()
    assert 'def test_' in source and 'page.goto' in source

def test_health_analyzer_handles_missing_report(tmp_path):
    result=HealingHealthAnalyzer(tmp_path/'missing.jsonl').analyze()
    assert result['total_events']==0 and result['healing_rate_percent']==0
