
class ElementSimilarity:

    # Importance assigned to each element attribute
    WEIGHTS = {
        "tag": 10,
        "id": 5,
        "name": 20,
        "type": 10,
        "aria_label": 20,
        "placeholder": 15,
        "text": 10,
        "href": 10
    }

    def calculate_similarity(self, original, candidate):

        total_weight = 0
        matched_weight = 0

        for attribute, weight in self.WEIGHTS.items():

            original_value = original.get(attribute)
            candidate_value = candidate.get(attribute)

            # Ignore attributes that were not available originally
            if not original_value:
                continue

            total_weight += weight

            if (
                candidate_value
                and str(original_value).strip().casefold()
                == str(candidate_value).strip().casefold()
            ):
                matched_weight += weight

        if total_weight == 0:
            return 0

        score = (matched_weight / total_weight) * 100

        return round(score, 2)

    def find_similar_elements(self, original, candidates):

        results = []

        for candidate in candidates:

            score = self.calculate_similarity(
                original,
                candidate
            )

            results.append({
                "element": candidate,
                "similarity": score
            })

        results.sort(
            key=lambda item: item["similarity"],
            reverse=True
        )

        return results
