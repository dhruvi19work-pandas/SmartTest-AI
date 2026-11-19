class MLFeatureExtractor:
    FEATURE_NAMES = ['similarity', 'locator_score', 'match_count', 'is_visible', 'is_id', 'is_name', 'is_aria_label', 'is_placeholder']

    def extract_features(self, candidate):
        strategy = str(candidate.get('strategy', '')).lower()
        return [
            float(candidate.get('similarity', 0)),
            float(candidate.get('locator_score', candidate.get('score', 0))),
            float(candidate.get('match_count', 0)),
            int(bool(candidate.get('is_visible', False))),
            int(strategy == 'id'), int(strategy == 'name'),
            int(strategy == 'aria-label'), int(strategy == 'placeholder')
        ]
