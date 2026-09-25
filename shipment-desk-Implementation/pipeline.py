# pipeline.py

from chains import classify_chain, draft_email_chain, escalate_chain
from tools import (
    calculate_damage_compensation,
    calculate_delay_compensation,
    calculate_lost_compensation,
)

STANDARD_ESCALATION_THRESHOLD = 200.0
PREMIUM_ESCALATION_THRESHOLD = 100.0


def process_exception(report_text: str, shipment_value: float, customer_tier: str) -> dict:
    log = []
    log.append(f"Starting triage for {customer_tier} customer (Shipment: ${shipment_value:.2f})")

    # 1. Classify
    raw_category = classify_chain.invoke({"report_text": report_text})
    category = raw_category.strip().lower()
    
    if category not in ["delayed", "damaged", "lost"]:
        category = "unknown"
    log.append(f"Classified exception as: '{category}'")

    # 2. Calculate Compensation
    if category == "delayed":
        comp = calculate_delay_compensation(shipment_value, report_text)
    elif category == "damaged":
        comp = calculate_damage_compensation(shipment_value, report_text)
    elif category == "lost":
        comp = calculate_lost_compensation(shipment_value, report_text)
    else:
        comp = {"amount": 0.0, "explanation": "Could not confidently classify this report."}

    amount = comp["amount"]
    explanation = comp["explanation"]
    log.append(f"Compensation calculated: ${amount:.2f} ({explanation})")

    # 3. Clean Escalation Decision (Adopted from Instructor)
    threshold = (
        PREMIUM_ESCALATION_THRESHOLD
        if customer_tier.strip().lower() == "premium"
        else STANDARD_ESCALATION_THRESHOLD
    )
    
    # Elegant boolean check
    needs_approval = (category == "unknown") or (amount > threshold)

    # 4. Draft Output (Keeping our superior context dictionaries)
    if needs_approval:
        # Generate the specific reason for the logs and the prompt
        reason = "Unclassifiable report." if category == "unknown" else f"Amount ${amount:.2f} exceeds ${threshold:.2f} threshold."
        log.append(f"Escalation triggered: {reason}")
        
        message_draft = escalate_chain.invoke({
            "category": category,
            "shipment_value": shipment_value,
            "customer_tier": customer_tier,
            "compensation_amount": amount,
            "reason": reason,
            "report_text": report_text,
        })
        outcome = "Escalated to Manager"
    else:
        log.append(f"Approved for auto-resolution (under ${threshold:.2f} threshold).")
        
        message_draft = draft_email_chain.invoke({
            "category": category,
            "compensation_amount": amount,
            "policy_note": explanation,
            "report_text": report_text,
        })
        outcome = "Auto-resolved"

    return {
        "category": category,
        "compensation_amount": amount,
        "needs_approval": needs_approval,
        "outcome": outcome,
        "reason": explanation,
        "message_draft": message_draft,
        "log": log,
    }