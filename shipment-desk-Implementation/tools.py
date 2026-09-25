# tools.py

# --- Global Constants for Business Rules ---
DELAY_URGENT_RATE = 0.10
DELAY_STANDARD_RATE = 0.05

DAMAGE_SEVERE_RATE = 0.50
DAMAGE_MODERATE_RATE = 0.25
DAMAGE_MINOR_RATE = 0.10

LOST_RATE = 1.00

# --- Expanded Keyword Lists ---
URGENT_DELAY_KEYWORDS = ["critical", "urgent", "asap", "time-sensitive"]
SEVERE_DAMAGE_KEYWORDS = ["destroyed", "total loss", "severely damaged", "crushed", "shattered", "unusable"]
MINOR_DAMAGE_KEYWORDS = ["cracked", "broken", "dent", "dented", "damaged", "scratched", "scuffed", "chipped"]


def calculate_delay_compensation(shipment_value: float, report_text: str = "") -> dict:
    """Delay compensation: 5% standard, 10% if urgent/critical."""
    text_lower = report_text.lower()
    
    if any(k in text_lower for k in URGENT_DELAY_KEYWORDS):
        rate = DELAY_URGENT_RATE
        explanation = "10% compensation for urgent/time-sensitive delay."
    else:
        rate = DELAY_STANDARD_RATE
        explanation = "5% standard compensation for delay."
    
    amount = round(shipment_value * rate, 2)
    return {"amount": amount, "explanation": explanation}


def calculate_damage_compensation(shipment_value: float, report_text: str = "") -> dict:
    """Damage compensation: scales with severity keywords."""
    text_lower = report_text.lower()
    
    if any(k in text_lower for k in SEVERE_DAMAGE_KEYWORDS):
        rate = DAMAGE_SEVERE_RATE
        explanation = "50% compensation for severe damage/total loss."
    elif any(k in text_lower for k in MINOR_DAMAGE_KEYWORDS):
        rate = DAMAGE_MODERATE_RATE
        explanation = "25% compensation for moderate to minor damage."
    else:
        rate = DAMAGE_MINOR_RATE
        explanation = "10% compensation for unspecified/minor damage."
    
    amount = round(shipment_value * rate, 2)
    return {"amount": amount, "explanation": explanation}


def calculate_lost_compensation(shipment_value: float, report_text: str = "") -> dict:
    """Lost shipment compensation: full 100% reimbursement."""
    amount = round(float(shipment_value) * LOST_RATE, 2)
    return {
        "amount": amount,
        "explanation": "100% reimbursement for lost shipment."
    }