from app.models import Feature

def wsjf_score(feature: Feature) -> float:
    if feature.job_size <= 0:
        return 0.0
    numerator = (feature.business_value + feature.time_criticality
                 + feature.risk_reduction)
    return numerator / feature.job_size

def rank_by_wsjf(features) -> list:
    ranked = sorted(features, key=wsjf_score, reverse=True)
    return [{"feature_id": f.id, "title": f.title,
             "wsjf_score": round(wsjf_score(f), 2),
             "business_value": f.business_value,
             "time_criticality": f.time_criticality,
             "risk_reduction": f.risk_reduction,
             "job_size": f.job_size}
            for f in ranked]
