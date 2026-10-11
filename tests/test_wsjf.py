from app.models import Feature
from app.core.wsjf import wsjf_score

def test_wsjf_score():
    f = Feature(id=1, title="A", business_value=10,
                time_criticality=5, risk_reduction=3, job_size=2)
    assert wsjf_score(f) == 9.0

def test_wsjf_zero_size():
    f = Feature(id=1, title="A", job_size=0)
    assert wsjf_score(f) == 0.0
