from app.models import Feature

PRIORITY = {
    "must_be": 1,
    "performance": 2,
    "attractive": 3,
    "indifferent": 4,
    "reverse": 5,
}

def kano_priority(feature: Feature) -> int:
    return PRIORITY.get(feature.kano_category, 5)

def rank_by_kano(features) -> list:
    ranked = sorted(features, key=kano_priority)
    return [{"feature_id": f.id, "title": f.title,
             "category": f.kano_category,
             "priority": kano_priority(f)} for f in ranked]

def kano_matrix(features) -> dict:
    matrix = {"must_be": [], "performance": [], "attractive": [],
              "indifferent": [], "reverse": []}
    for f in features:
        matrix.setdefault(f.kano_category, []).append(f.title)
    return matrix
