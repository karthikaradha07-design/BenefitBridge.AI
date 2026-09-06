from typing import List, Dict

def evaluate(profile, scheme: dict):
    score = 0
    reasons: List[str] = []
    age_ok = scheme["min_age"] <= profile.age <= scheme["max_age"]
    if age_ok:
        score += 25; reasons.append("Age falls within the listed age range.")
    else:
        reasons.append("Age does not fall within the listed age range.")
    occupation = profile.occupation.lower()
    occs = [x.lower() for x in scheme.get("occupations", [])]
    if "any" in occs or occupation in occs:
        score += 25; reasons.append("Your occupation matches the scheme profile.")
    else:
        reasons.append("Your occupation may not match the scheme profile.")
    genders = [x.lower() for x in scheme.get("genders", [])]
    if "any" in genders or profile.gender.lower() in genders:
        score += 15; reasons.append("Gender requirement matches.")
    else:
        reasons.append("Gender requirement may not match.")
    if scheme.get("income_max") is None or profile.annual_income is None:
        score += 10; reasons.append("Income is not used as a hard exclusion in this demo.")
    elif profile.annual_income <= scheme["income_max"]:
        score += 20; reasons.append("Annual income is within the listed ceiling.")
    else:
        reasons.append("Annual income is above the listed ceiling.")
    events = {e.lower() for e in profile.life_events}
    scheme_events = {e.lower() for e in scheme.get("life_events", [])}
    if events and events.intersection(scheme_events):
        score += 15; reasons.append("Your selected life event is relevant to this scheme.")
    elif not events:
        score += 5
    else:
        reasons.append("Your selected life events do not directly match the scheme category.")
    if profile.state.lower() in ("all india", "any", scheme.get("state", "").lower()):
        score += 10; reasons.append("The scheme covers your state or is listed as pan-India.")
    else:
        reasons.append("State coverage should be verified before applying.")
    return min(score, 100), reasons


def rank(profile, candidates: List[dict]):
    out = []
    for s in candidates:
        score, reasons = evaluate(profile, s)
        item = dict(s)
        item["score"] = score
        item["reasons"] = reasons
        out.append(item)
    return sorted(out, key=lambda x: (x["score"], x.get("retrieval_score", 0)), reverse=True)
