"""Dependency-free CART-style decision tree trainer for locator reliability."""
import csv, json
from pathlib import Path
from intelligence.ml.feature_extractor import MLFeatureExtractor

ROOT = Path(__file__).resolve().parents[2]
DATA_FILE = ROOT / 'intelligence' / 'ml' / 'locator_training_data.csv'
MODEL_FILE = ROOT / 'intelligence' / 'ml' / 'locator_model.json'

class LocatorModelTrainer:
    def __init__(self): self.extractor = MLFeatureExtractor()
    def load_training_data(self):
        X, y = [], []
        with DATA_FILE.open(encoding='utf-8-sig', newline='') as f:
            for row in csv.DictReader(f):
                X.append([float(row[k]) for k in self.extractor.FEATURE_NAMES]); y.append(int(row['label']))
        if not X or len(set(y)) < 2: raise ValueError('Training CSV must contain examples for both labels 0 and 1.')
        return X, y
    @staticmethod
    def gini(labels):
        if not labels: return 0.0
        return 1 - sum((labels.count(c)/len(labels))**2 for c in set(labels))
    @staticmethod
    def majority(labels): return int(sum(labels) >= len(labels)/2)
    def build_tree(self, X, y, depth=0, max_depth=4, min_samples=1):
        if len(set(y)) == 1 or depth >= max_depth or len(y) < min_samples:
            return {'type':'leaf','prediction':self.majority(y),'samples':len(y)}
        parent = self.gini(y); best = None; best_gain = 0
        for j, name in enumerate(self.extractor.FEATURE_NAMES):
            vals = sorted(set(row[j] for row in X))
            for t in [(a+b)/2 for a,b in zip(vals, vals[1:])]:
                li = [i for i,r in enumerate(X) if r[j] <= t]; ri = [i for i,r in enumerate(X) if r[j] > t]
                if not li or not ri: continue
                ly=[y[i] for i in li]; ry=[y[i] for i in ri]
                gain=parent-(len(ly)/len(y)*self.gini(ly)+len(ry)/len(y)*self.gini(ry))
                if gain > best_gain: best_gain=gain; best=(j,t,li,ri)
        if best is None: return {'type':'leaf','prediction':self.majority(y),'samples':len(y)}
        j,t,li,ri=best
        return {'type':'split','feature':self.extractor.FEATURE_NAMES[j],'feature_index':j,'threshold':t,
                'left':self.build_tree([X[i] for i in li],[y[i] for i in li],depth+1,max_depth,min_samples),
                'right':self.build_tree([X[i] for i in ri],[y[i] for i in ri],depth+1,max_depth,min_samples)}
    def predict(self, tree, row):
        if tree['type']=='leaf': return tree['prediction']
        branch='left' if row[tree['feature_index']] <= tree['threshold'] else 'right'
        return self.predict(tree[branch], row)
    def train(self):
        X,y=self.load_training_data(); model=self.build_tree(X,y)
        MODEL_FILE.write_text(json.dumps(model,indent=2),encoding='utf-8'); return model
    def evaluate(self):
        X,y=self.load_training_data(); pred=[]
        for i in range(len(y)):
            tx=[r for j,r in enumerate(X) if j!=i]; ty=[v for j,v in enumerate(y) if j!=i]
            pred.append(self.predict(self.build_tree(tx,ty),X[i]))
        correct=sum(a==b for a,b in zip(y,pred)); tp=sum(a==1 and b==1 for a,b in zip(y,pred)); tn=sum(a==0 and b==0 for a,b in zip(y,pred))
        return {'method':'leave-one-out cross-validation','samples':len(y),'correct':correct,'accuracy_percent':round(correct/len(y)*100,2),'true_positive':tp,'true_negative':tn,'false_positive':sum(a==0 and b==1 for a,b in zip(y,pred)),'false_negative':sum(a==1 and b==0 for a,b in zip(y,pred)), 'warning':'Tiny illustrative dataset; metrics are not evidence of production performance.'}
if __name__=='__main__':
    trainer=LocatorModelTrainer(); print(json.dumps(trainer.evaluate(),indent=2)); trainer.train(); print(f'Model saved: {MODEL_FILE}')
