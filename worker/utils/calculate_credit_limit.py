import logging
import numpy as np
from store.transaction_store import get_recent_transactions


def process_emotional_data(user_id, primary_emotion, intensity, duration, context):
    recent_transactions = get_recent_transactions(user_id)
    if not recent_transactions:
        logging.warning(f"No transactions found for user {user_id}")
        return None

    risk_score = calculate_risk_score(
        user_id,
        primary_emotion,
        intensity,
        duration,
        context,
        recent_transactions,
    )

    return risk_score


def calculate_risk_score(
    user_id,
    primary_emotion,
    intensity,
    duration,
    context,
    transactions,
):
    features = {
        "user_id": user_id,
        "primary_emotion": primary_emotion,
        "intensity": intensity,
        "duration": duration,
        "context": context,
        "transaction_history": transactions
    }

    risk_score = predict_risk_score(features)
    return risk_score


def predict_risk_score(features):
    # intensity = features.get("intensity", 0)
    primary_emotion = features.get("primary_emotion", "neutral")
    transaction_history = features.get("transaction_history", [])

    income_total = sum(
        [trans["amount"] for trans in transaction_history if trans["amount"] > 0],
    )
    spending_total = sum(
        [abs(trans["amount"]) for trans in transaction_history if trans["amount"] < 0],
    )
    balance_fluctuation = np.std(
        [trans["balance_after_transaction"] for trans in transaction_history],
    )

    if primary_emotion in ["anger", "anxiety", "stress"]:
        emotional_factor = 0.7
    elif primary_emotion in ["happiness", "calm"]:
        emotional_factor = 0.3
    else:
        emotional_factor = 0.5

    financial_factor = (spending_total / (income_total + 1))

    risk_score = emotional_factor * 0.5
    + (financial_factor * 0.3) + (balance_fluctuation / 1000) * 0.2

    risk_score = max(0, min(risk_score, 1))

    return risk_score
