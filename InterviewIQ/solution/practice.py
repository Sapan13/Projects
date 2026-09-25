FILLER_WORDS = ["um", "uh", "like", "basically", "actually", "you know", "so yeah", "i mean"]

def detect_filler_words(answer: str) -> dict:
    """Count filler words (um, like, basically, etc.) in a candidate's answer."""
    text = answer.lower()
    found = {w: text.count(w) for w in FILLER_WORDS if text.count(w) > 0}
    total = sum(found.values())
    return {
        "total": total,
        "found": found,
        "verdict": "clean" if total <= 2 else "needs improvement",
    }
    
STAR_SIGNALS = {
    "situation": ["when", "at my", "in my previous", "while working", "during"],
    "task": ["i needed to", "my task", "i was responsible", "the goal was", "i had to"],
    "action": ["i decided", "i implemented", "i built", "i led", "i created", "i took"],
    "result": ["as a result", "this led to", "we achieved", "the outcome", "ended up", "improved", "increased", "reduced"],
}
    
def check_star_structure(answer: str) -> dict:
    """Check whether a behavioral answer covers Situation, Task, Action, Result."""
    text = answer.lower()
    present = {stage: any(sig in text for sig in signals) for stage, signals in STAR_SIGNALS.items()}
    missing = [stage for stage, ok in present.items() if not ok]
    return {
        "present": present,
        "missing": missing,
        "all_present": not missing
    }
    
result = check_star_structure("When I was at my previous job")
print(result)