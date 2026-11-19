
from playwright.sync_api import Page


class ElementInspector:

    def __init__(self, page: Page):
        self.page = page

    def inspect_elements(self):
        elements = self.page.locator(
            "input, button, a, select, textarea"
        )

        element_data = elements.evaluate_all("""
            elements => elements
                .filter(element => {
                    const style = window.getComputedStyle(element);

                    return (
                        element.getClientRects().length > 0 &&
                        style.visibility !== "hidden" &&
                        style.display !== "none"
                    );
                })
                .map(element => ({
                    tag: element.tagName.toLowerCase(),
                    id: element.id,
                    name: element.getAttribute("name"),
                    type: element.getAttribute("type"),
                    placeholder: element.getAttribute("placeholder"),
                    aria_label: element.getAttribute("aria-label"),
                    role: element.getAttribute("role"),
                    text: element.innerText.trim(),
                    href: element.getAttribute("href")
                }))
        """)

        return element_data
