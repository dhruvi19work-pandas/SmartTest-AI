from intelligence.element_inspector import ElementInspector
from intelligence.locator_ranker import LocatorRanker
from intelligence.locator_strategies import LocatorStrategies
from intelligence.element_similarity import ElementSimilarity
from intelligence.confidence_scorer import ConfidenceScorer

class SmartLocatorEngine:
    """Combines deterministic validation/confidence with an optional ML ranking signal."""
    def __init__(self, page, use_ml=True):
        self.page=page; self.inspector=ElementInspector(page); self.ranker=LocatorRanker()
        self.strategies=LocatorStrategies(page); self.similarity=ElementSimilarity(); self.scorer=ConfidenceScorer()
        self.predictor=None
        if use_ml:
            try:
                from intelligence.ml.locator_predictor import LocatorPredictor
                self.predictor=LocatorPredictor()
            except (ImportError, OSError, ValueError, FileNotFoundError):
                self.predictor=None
    def find_best_locator(self, original_element):
        results=[]
        for element in self.inspector.inspect_elements():
            similarity=self.similarity.calculate_similarity(original_element,element)
            if similarity < 50: continue
            for candidate in self.ranker.rank_element(element):
                locator=self.page.locator(candidate['locator'])
                validation=self.strategies.validate_locator(candidate['strategy'],locator)
                confidence=self.scorer.calculate_confidence(similarity,candidate['score'],validation['count'],validation['visible'])
                features={'similarity':similarity,'locator_score':candidate['score'],'match_count':validation['count'],
                          'is_visible':validation['visible'],'strategy':candidate['strategy']}
                prediction=self.predictor.predict(features) if self.predictor else None
                # ML is an additional ranking signal, never a substitute for uniqueness/visibility checks.
                usable=validation['usable'] and confidence['recommended']
                results.append({'element':element,'strategy':candidate['strategy'],'locator':candidate['locator'],
                    'similarity':similarity,'locator_score':candidate['score'],'match_count':validation['count'],
                    'is_visible':validation['visible'],'confidence':confidence['confidence'],'level':confidence['level'],
                    'ml_prediction':prediction,'ml_enabled':self.predictor is not None,
                    'recommended':bool(usable and (prediction in (None,1)))})
        results.sort(key=lambda x:(x['recommended'], x['confidence'], x['ml_prediction']==1),reverse=True)
        return results
    def get_best_locator(self, original_element):
        return next((r for r in self.find_best_locator(original_element) if r['recommended']),None)

# Backwards-compatible name used by an earlier test/module.
LocatorEngine = SmartLocatorEngine
