from typing import List, Tuple
from mentees.models import Mentee
from mentors.models import Mentor


def score_match(mentee: Mentee, mentor: Mentor) -> Tuple[int, str, dict]:
    """Return (overall_score, reasoning, components)."""
    # Component scores 0-100
    business_stage = 100 if mentor.business_stage_expertise == mentee.business_stage else 0
    industry = 100 if mentor.industry.lower() == mentee.industry.lower() else 0

    # Simple text overlaps
    challenge = 0
    for word in mentee.main_challenges.lower().split(','):
        if word.strip() and word.strip() in mentor.key_focus_areas.lower():
            challenge = 100
            break

    goals = 0
    for word in mentee.mentorship_goals.lower().split(','):
        if word.strip() and word.strip() in mentor.key_focus_areas.lower():
            goals = 100
            break

    # Availability and rating boost
    availability_boost = 10 if mentor.availability_status == 'available' else 0
    rating_boost = min(int(mentor.average_rating * 2), 10) if hasattr(mentor, 'average_rating') else 0

    weights = {
        'business_stage': 0.30,
        'industry': 0.25,
        'challenge': 0.25,
        'goals': 0.20,
    }

    base = int(
        business_stage * weights['business_stage'] +
        industry * weights['industry'] +
        challenge * weights['challenge'] +
        goals * weights['goals']
    )
    overall = min(100, base + availability_boost + rating_boost)

    reasoning = (
        f"Stage: {business_stage}/100, Industry: {industry}/100, "
        f"Challenges: {challenge}/100, Goals: {goals}/100, "
        f"Boosts: {availability_boost + rating_boost}"
    )

    components = {
        'business_stage': business_stage,
        'industry': industry,
        'challenge': challenge,
        'goals': goals,
        'availability_boost': availability_boost,
        'rating_boost': rating_boost,
    }
    return overall, reasoning, components


def top_matches(mentee: Mentee, limit: int = 3) -> List[Tuple[Mentor, int, str]]:
    mentors = Mentor.objects.filter(is_active=True, is_verified=True)
    scored = []
    for m in mentors:
        score, reasoning, _ = score_match(mentee, m)
        scored.append((m, score, reasoning))
    scored.sort(key=lambda x: x[1], reverse=True)
    return scored[:limit]



