"""Template-based test scaffold generator; no external LLM/API required."""
from pathlib import Path
import re

class ScenarioGenerator:
    def generate_login_tests(self, page_name='generated_login'):
        safe=re.sub(r'[^a-zA-Z0-9_]+','_',page_name).strip('_').lower() or 'generated_login'
        return f'''import pytest\n\n@pytest.mark.smoke\ndef test_{safe}_page_loads(page):\n    page.goto("https://the-internet.herokuapp.com/login")\n    assert page.locator("#username").is_visible()\n    assert page.locator("#password").is_visible()\n    assert page.locator("button[type='submit']").is_visible()\n\n@pytest.mark.regression\ndef test_{safe}_invalid_login_shows_error(page):\n    page.goto("https://the-internet.herokuapp.com/login")\n    page.locator("#username").fill("invalid-user")\n    page.locator("#password").fill("invalid-password")\n    page.locator("button[type='submit']").click()\n    assert "Your username is invalid!" in page.locator("#flash").inner_text()\n'''
    def write(self, output='tests/generated_login_tests.py'):
        path=Path(output); path.parent.mkdir(parents=True,exist_ok=True); path.write_text(self.generate_login_tests(),encoding='utf-8'); return path
if __name__=='__main__': print(f'Generated: {ScenarioGenerator().write()}')
