from intelligence.ml.model_trainer import LocatorModelTrainer
from intelligence.ml.locator_predictor import LocatorPredictor

def test_training_data_has_both_classes():
    X,y=LocatorModelTrainer().load_training_data()
    assert len(X)==len(y)>=8 and set(y)=={0,1}

def test_model_trains_and_predicts():
    trainer=LocatorModelTrainer(); tree=trainer.train()
    predictor=LocatorPredictor()
    result=predictor.predict({'similarity':100,'locator_score':100,'match_count':1,'is_visible':True,'strategy':'id'})
    assert result in (0,1)
    assert tree['type'] in ('leaf','split')

def test_evaluation_returns_metrics():
    metrics=LocatorModelTrainer().evaluate()
    assert metrics['samples'] >= 8
    assert 0 <= metrics['accuracy_percent'] <= 100
