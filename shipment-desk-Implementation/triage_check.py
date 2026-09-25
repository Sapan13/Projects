# triage_check.py

from pipeline import process_exception


def run_checks():
    scenarios = [
        {
            "name": "Mild Delay",
            "report": "My package arrived 2 days later than expected.",
            "value": 50.0,
            "tier": "standard",
            "expected_category": "delayed",
            "expected_escalation": False  # $2.50 comp < $200 standard threshold
        },
        {
            "name": "High-value Loss",
            "report": "Tracking says delivered but I never got it. It's totally lost.",
            "value": 500.0,
            "tier": "premium",
            "expected_category": "lost",
            "expected_escalation": True   # $500 comp > $100 premium threshold
        },
        {
            "name": "Minor Damage Claim",
            "report": "The box has a small dent on the corner.",
            "value": 100.0,
            "tier": "standard",
            "expected_category": "damaged",
            "expected_escalation": False  # $10.00 comp < $200 standard threshold
        },
        {
            "name": "Garbled/Unclassifiable Report",
            "report": "fhjsdkfhkjsdhfjkdshf",
            "value": 10.0,
            "tier": "standard",
            "expected_category": "unknown",
            "expected_escalation": True   # Unknown categories must auto-escalate
        }
    ]

    print("--- Running Triage Checks ---")
    all_passed = True

    for s in scenarios:
        print(f"\nTesting: {s['name']}")
        
        # Run the pipeline
        result = process_exception(s["report"], s["value"], s["tier"])
        
        # Check assertions
        cat_match = result["category"] == s["expected_category"]
        esc_match = result["needs_approval"] == s["expected_escalation"]
        
        print(f"  Category: {result['category']} (Expected: {s['expected_category']}) -> {'✅ PASS' if cat_match else '❌ FAIL'}")
        print(f"  Escalated: {result['needs_approval']} (Expected: {s['expected_escalation']}) -> {'✅ PASS' if esc_match else '❌ FAIL'}")

        if not (cat_match and esc_match):
            all_passed = False

    print("\n-----------------------------")
    if all_passed:
        print("🎉 ALL CHECKS PASSED! Your pipeline routing is correct.")
    else:
        print("⚠️ SOME CHECKS FAILED. Review your pipeline.py logic.")

if __name__ == "__main__":
    run_checks()