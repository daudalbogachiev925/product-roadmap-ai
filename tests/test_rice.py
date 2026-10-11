from app.models import Feature
from app.core.rice import rice_score, rank_by_rice

def test_rice_basic():
    f = Feature(id=1, title="A", reach=1000, impact=2.0,
                confidence=0.9, effort=4.0)
    assert rice_score(f) == pytest.approx(450.0)

def test_rice_zero_effort():
    f = Feature(id=1, title="A", reach=1000, impact=2.0,
                confidence=0.9, effort=0)
    assert rice_score(f) == 0.0

def test_rank_by_rice():
    a = Feature(id=1, title="A", reach=100, impact=3, confidence=1, effort=1)
    b = Feature(id=2, title="B", reach=100, impact=3, confidence=1, effort=5)
    result = rank_by_rice([a, b])
    assert result[0]["feature_id"] == 1


import pytest
