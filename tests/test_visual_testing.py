import pytest
PIL=pytest.importorskip('PIL')
from PIL import Image
from visual_testing.visual_regression import compare, BASELINES, ACTUAL

def test_visual_comparison_identical_images(tmp_path, monkeypatch):
    import visual_testing.visual_regression as vr
    monkeypatch.setattr(vr,'BASELINES',tmp_path/'base'); monkeypatch.setattr(vr,'ACTUAL',tmp_path/'actual'); monkeypatch.setattr(vr,'DIFFS',tmp_path/'diff')
    vr.BASELINES.mkdir(); vr.ACTUAL.mkdir(); vr.DIFFS.mkdir()
    image=Image.new('RGBA',(4,4),(255,255,255,255)); image.save(vr.BASELINES/'sample.png'); image.save(vr.ACTUAL/'sample.png')
    assert vr.compare('sample')['match'] is True
