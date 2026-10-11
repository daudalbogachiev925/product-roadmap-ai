from app.models import Feature

def rice_score(feature: Feature) -> float:
    if feature.effort <= 0:
        return 0.0
    return (feature.reach * feature.impact * feature.confidence) / feature.effort

def rank_by_rice(features) -> list:
    ranked = sorted(features, key=rice_score, reverse=True)
    return [{"feature_id": f.id, "title": f.title,
             "rice_score": round(rice_score(f), 2),
             "reach": f.reach, "impact": f.impact,
             "confidence": f.confidence, "effort": f.effort}
            for f in ranked]
