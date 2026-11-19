
class ConfidenceScorer:

    def calculate_confidence(
        self,
        similarity_score,
        locator_score,
        match_count,
        is_visible
    ):

        # Reject ambiguous or invisible elements
        if match_count != 1 or not is_visible:
            return {
                "confidence": 0,
                "level": "LOW",
                "recommended": False
            }

        # Weighted confidence calculation
        confidence = (
            similarity_score * 0.60
            + locator_score * 0.25
            + 100 * 0.15
        )

        confidence = round(confidence, 2)

        if confidence >= 85:
            level = "HIGH"
        elif confidence >= 70:
            level = "MEDIUM"
        else:
            level = "LOW"

        return {
            "confidence": confidence,
            "level": level,
            "recommended": confidence >= 85
        }
