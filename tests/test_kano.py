from app.models import Feature
from app.core.kano import rank_by_kano, kano_priority

def test_kano_priority_order():
    must = Feature(id=1, title="must", kano_category="must_be")
    perf = Feature(id=2, title="perf", kano_category="performance")
    att = Feature(id=3, title="att", kano_category="attractive")
    assert kano_priority(must) < kano_priority(perf) < kano_priority(att)

def test_rank_by_kano():
    features = [
        Feature(id=1, title="x", kano_category="attractive"),
        Feature(id=2, title="y", kano_category="must_be"),
    ]
    result = rank_by_kano(features)
    assert result[0]["feature_id"] == 2
