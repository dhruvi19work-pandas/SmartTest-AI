
from playwright.sync_api import Error as PlaywrightError

from intelligence.locator_engine import SmartLocatorEngine
from intelligence.healing_reporter import HealingReporter
from core.logger import get_logger


class SelfHealingHandler:

    CONFIDENCE_THRESHOLD = 85

    def __init__(self, page):
        self.page = page
        self.engine = SmartLocatorEngine(page)
        self.reporter = HealingReporter()
        self.logger = get_logger("SelfHealingHandler")

    def heal_locator(self, original_element):

        self.logger.info("Starting locator healing process")

        results = self.engine.find_best_locator(original_element)

        if not results:
            self.reporter.record_event(
                original_element,
                status="FAILED",
                reason="No replacement found"
            )

            self.logger.warning("No replacement locator found")
            return None

        if isinstance(results, list):

            valid_results = [
                item for item in results
                if isinstance(item, dict)
                and "confidence" in item
            ]

            if not valid_results:
                self.reporter.record_event(
                    original_element,
                    status="FAILED",
                    reason="No valid candidates found"
                )
                return None

            result = max(
                valid_results,
                key=lambda item: item["confidence"]
            )

        else:
            result = results

        confidence = result["confidence"]
        replacement = result.get("locator")

        if (
            confidence < self.CONFIDENCE_THRESHOLD
            or not result.get("recommended", False)
        ):
            self.reporter.record_event(
                original_element,
                replacement_locator=replacement,
                confidence=confidence,
                status="REJECTED",
                reason="Confidence below threshold or not recommended"
            )

            self.logger.warning("Replacement rejected")
            return None

        healed_locator = self.page.locator(replacement)

        if (
            healed_locator.count() != 1
            or not healed_locator.is_visible()
        ):
            self.reporter.record_event(
                original_element,
                replacement_locator=replacement,
                confidence=confidence,
                status="FAILED",
                reason="Replacement failed final validation"
            )

            return None

        self.reporter.record_event(
            original_element,
            replacement_locator=replacement,
            confidence=confidence,
            status="HEALED",
            reason="Replacement uniquely located and visible"
        )
        self.logger.info("Locator successfully healed: %s", replacement)
        return healed_locator

    def fill_with_healing(
        self,
        original_locator,
        original_element,
        value
    ):

        try:
            self.logger.info(
                "Trying original locator: %s",
                original_locator
            )

            self.page.locator(original_locator).fill(value)

            self.logger.info("Original locator worked")
            return True

        except PlaywrightError:

            self.logger.warning(
                "Original locator failed. Starting healing."
            )

            healed_locator = self.heal_locator(
                original_element
            )

            if healed_locator is None:
                self.logger.error("Healing failed")
                raise

            self.logger.info("Retrying fill with healed locator")

            healed_locator.fill(value)

            self.logger.info("Fill operation succeeded after healing")
            return True
