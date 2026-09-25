# session.py

triage_log = []

def add_to_log(exception_result: dict):
    """Appends a processed exception to the daily log."""
    triage_log.append(exception_result)

def generate_daily_summary() -> dict:
    """Calculates real aggregation metrics across all processed exceptions."""
    if not triage_log:
        return {
            "total_compensation": 0.0,
            "escalation_rate": "0.0%",
            "costliest_category": "None"
        }

    total_compensation = sum(item.get("compensation_amount", 0.0) for item in triage_log)
    
    escalated_count = sum(1 for item in triage_log if item.get("needs_approval", False))
    escalation_rate = (escalated_count / len(triage_log)) * 100

    # Group compensation by category to find the costliest one
    category_totals = {}
    for item in triage_log:
        cat = item.get("category", "unknown")
        comp = item.get("compensation_amount", 0.0)
        category_totals[cat] = category_totals.get(cat, 0.0) + comp

    # Find the category with the maximum total compensation
    if category_totals:
        costliest_category = max(category_totals, key=category_totals.get) # type: ignore
    else:
        costliest_category = "None"

    return {
        "total_compensation": round(total_compensation, 2),
        "escalation_rate": f"{escalation_rate:.1f}%",
        "costliest_category": costliest_category
    }