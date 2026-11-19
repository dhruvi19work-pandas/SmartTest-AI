# SmartTest AI — Self-Healing Test Automation Framework

A portfolio project combining Python, Playwright and pytest with smart locator discovery, guarded self-healing, a dependency-free decision-tree experiment, template-based test scaffolding, screenshot regression utilities, healing analytics and CI.

> **Honest scope:** the included locator dataset is a tiny illustrative dataset. The decision tree demonstrates a trainable ML workflow, not production-grade model quality. Test generation is deterministic/template-based (not an LLM). Visual comparison uses pixel differences and requires Pillow. Review and execute the test suite in your own environment before describing measured results on a resume.

## Features
- Page Object Model and reusable browser management.
- Element inspection, weighted similarity, locator strategy generation and uniqueness/visibility validation.
- Self-healing fill operation with JSONL event history.
- Optional decision-tree ranking signal implemented in pure Python (no NumPy/scikit-learn dependency).
- Leave-one-out evaluation utility for the sample dataset.
- Template-based pytest scenario scaffold generation.
- Screenshot baseline capture and pixel-difference comparison.
- Local healing dashboard and maintenance summary.
- GitHub Actions CI workflow.

## Requirements
Python 3.10+ (CI uses 3.12), a supported browser, and Windows/macOS/Linux.

```bash
python -m venv .venv
# Windows PowerShell: .venv\Scripts\Activate.ps1
# macOS/Linux: source .venv/bin/activate
python -m pip install -r requirements.txt
python -m playwright install chromium
copy .env.example .env   # Windows; on macOS/Linux use: cp .env.example .env
```

Set `BASE_URL`, `BROWSER`, `BROWSER_CHANNEL`, and `HEADLESS` in `.env`. For standard Playwright Chromium, leave `BROWSER_CHANNEL` blank. For installed Microsoft Edge, set `BROWSER_CHANNEL=msedge`.

## Run
```bash
python -m pytest -m 'not visual'
python -m pytest --html=reports/pytest-report.html --self-contained-html
python -m intelligence.ml.model_trainer
python -m test_generator.scenario_generator
python -m dashboard.app
```
Open the dashboard at `http://127.0.0.1:8765`.

## Visual regression usage
```python
from visual_testing.visual_regression import capture, compare

# First run: capture baseline
capture(page, 'login', baseline=True)
# Later run: capture current image and compare
capture(page, 'login')
result = compare('login', threshold=0.001)
assert result['match'], result
```
Baseline images are intentionally not committed by default; review and commit approved baselines when adopting this feature.

## ML experiment
Training data: `intelligence/ml/locator_training_data.csv`.
Train and evaluate: `python -m intelligence.ml.model_trainer`.
The CSV contains only eight synthetic examples. Do not report its cross-validation score as evidence of generalization. Collect representative labelled locator outcomes before making performance claims.

## Project layout
```text
config/ core/ pages/ tests/
intelligence/          # inspection, similarity, ranking, healing
intelligence/ml/       # feature extraction, tree trainer, predictor, sample data
visual_testing/        # screenshot capture and image diff
 test_generator/       # deterministic pytest scaffold generator
maintenance/           # healing analytics
 dashboard/             # local report dashboard
.github/workflows/     # CI
reports/                # runtime reports (ignored by Git)
```

## Resume-ready description (use only after verifying locally)
**SmartTest AI — Intelligent Self-Healing Test Automation Framework**
- Built a Python/Playwright/pytest automation framework using Page Object Model and reusable browser fixtures.
- Implemented DOM element inspection, attribute similarity matching, multi-strategy locator generation, and uniqueness/visibility validation.
- Developed a self-healing workflow with confidence gating, optional decision-tree candidate classification, and structured healing telemetry.
- Added screenshot baseline comparison, test-scaffold generation, healing analytics dashboard, and GitHub Actions CI.

## Limitations / next improvements
- Replace synthetic ML examples with a larger, independently labelled dataset and holdout evaluation.
- Add LLM-backed test generation only with explicit provider configuration and secure API-key handling.
- Add stable visual baselines per OS/browser and tune pixel tolerance for rendering differences.
- Add authenticated dashboard access before exposing it beyond localhost.
