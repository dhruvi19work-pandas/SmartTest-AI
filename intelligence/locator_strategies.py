
class LocatorStrategies:

    def __init__(self, page):
        self.page = page

    def validate_locator(self, strategy, locator):

        count = locator.count()

        visible = (
            locator.is_visible()
            if count == 1
            else False
        )

        return {
            "strategy": strategy,
            "count": count,
            "visible": visible,
            "usable": count == 1 and visible
        }

    def find_username_candidates(self):

        candidates = [
            (
                "ID",
                self.page.locator("#username")
            ),
            (
                "Name",
                self.page.locator("input[name='username']")
            ),
            (
                "Label",
                self.page.get_by_label("Username")
            ),
            (
                "Role",
                self.page.get_by_role(
                    "textbox",
                    name="Username"
                )
            )
        ]

        results = []

        for strategy, locator in candidates:

            result = self.validate_locator(
                strategy,
                locator
            )

            results.append(result)

        return results

class LocatorStrategies:

    def __init__(self, page):
        self.page = page

    def validate_locator(self, strategy, locator):

        count = locator.count()

        visible = (
            locator.is_visible()
            if count == 1
            else False
        )

        return {
            "strategy": strategy,
            "count": count,
            "visible": visible,
            "usable": count == 1 and visible
        }

    def find_username_candidates(self):

        candidates = [
            (
                "ID",
                self.page.locator("#username")
            ),
            (
                "Name",
                self.page.locator("input[name='username']")
            ),
            (
                "Label",
                self.page.get_by_label("Username")
            ),
            (
                "Role",
                self.page.get_by_role(
                    "textbox",
                    name="Username"
                )
            )
        ]

        results = []

        for strategy, locator in candidates:

            result = self.validate_locator(
                strategy,
                locator
            )

            results.append(result)

        return results
