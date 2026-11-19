
class LocatorRanker:

    def rank_element(self, element):
        candidates = []

        # ID is generally a strong locator
        if element.get("id"):
            candidates.append({
                "strategy": "id",
                "locator": f"#{element['id']}",
                "score": 100
            })

        # Name attribute
        if element.get("name"):
            candidates.append({
                "strategy": "name",
                "locator": f"{element['tag']}[name='{element['name']}']",
                "score": 90
            })

        # Accessible label
        if element.get("aria_label"):
            candidates.append({
                "strategy": "aria-label",
                "locator": f"[aria-label='{element['aria_label']}']",
                "score": 95
            })

        # Placeholder
        if element.get("placeholder"):
            candidates.append({
                "strategy": "placeholder",
                "locator": f"[placeholder='{element['placeholder']}']",
                "score": 85
            })

        # Visible text
        if element.get("text"):
            candidates.append({
                "strategy": "text",
                "locator": f"text={element['text']}",
                "score": 70
            })

        # Sort candidates from highest to lowest score
        candidates.sort(
            key=lambda candidate: candidate["score"],
            reverse=True
        )

        return candidates
