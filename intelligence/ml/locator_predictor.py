import json
from intelligence.ml.model_trainer import MODEL_FILE, LocatorModelTrainer
from intelligence.ml.feature_extractor import MLFeatureExtractor

class LocatorPredictor:
    def __init__(self, model_path=MODEL_FILE):
        self.extractor=MLFeatureExtractor(); self.model_path=model_path
        if not model_path.exists(): LocatorModelTrainer().train()
        self.model=json.loads(model_path.read_text(encoding='utf-8'))
    def predict(self, candidate):
        row=self.extractor.extract_features(candidate)
        return LocatorModelTrainer().predict(self.model,row)
