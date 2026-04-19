def calculate_patient(adherence, missed_doses, age):
    # Base logic
    if adherence >= 95:
        risk = "Low"
        heart_rate = 72
        bp = "120/80"

    elif adherence >= 80:
        risk = "Moderate"
        heart_rate = 82
        bp = "128/84"

    elif adherence >= 60:
        risk = "High"
        heart_rate = 95
        bp = "140/90"

    else:
        risk = "Critical"
        heart_rate = 105
        bp = "150/100"

    # Age effect
    if age > 60:
        heart_rate += 5

    # Missed dose effect
    heart_rate += missed_doses * 3

    # Severe missed doses escalation
    if missed_doses >= 4:
        risk = "Critical"

    return {
        "risk_level": risk,
        "heart_rate": heart_rate,
        "blood_pressure": bp
    }