import numpy as np
from config import logger

from store.transaction_store import get_recent_transactions


def get_credit_limit(user_id, primary_emotion, intensity, context):
    recent_transactions = get_recent_transactions(user_id)
    if not recent_transactions:
        logger.warning(f"No transactions found for user {user_id}")
        return None

    # Calculate the risk score based on user's emotion and transactions
    total_income, total_spending, risk_score = predict_risk_score(
        primary_emotion,
        intensity,
        recent_transactions,
    )
    logger.info(f"Calculated risk score: {risk_score}")

    # Calculate the base credit limit based on transaction history
    base_credit_limit = calculate_base_credit_limit(
        total_income,
        total_spending,
        recent_transactions,
    )
    logger.info(f"Calculated total income: {total_income}")
    logger.info(f"Calculated total spending: {total_spending}")
    logger.info(f"Calculated base credit limit: {base_credit_limit}")

    # Adjust the final credit limit based on the risk score
    final_credit_limit = base_credit_limit * (1 - risk_score)

    return risk_score, final_credit_limit


def predict_risk_score(primary_emotion, intensity, transactions):
    total_income = sum(
        [trans["amount"] for trans in transactions if trans["amount"] > 0],
    )
    total_spending = sum(
        [abs(trans["amount"]) for trans in transactions if trans["amount"] < 0],
    )
    balance_fluctuation = np.std(
        [trans["balance_after_transaction"] for trans in transactions],
    )

    # Determine the emotional factor based on the user's primary emotion
    if primary_emotion in ["anger", "anxiety", "stress"]:
        emotional_factor = 0.7
    elif primary_emotion in ["happiness", "calm"]:
        emotional_factor = 0.3
    else:
        emotional_factor = 0.5

    # Scale the emotional factor by the intensity of the emotion
    emotional_factor *= intensity
    # Calculate the financial factor based on income and spending ratio
    financial_factor = total_spending / (total_income + 1)

    risk_score = (emotional_factor * 0.5) + (financial_factor * 0.3)
    + (balance_fluctuation / 1000) * 0.2

    return total_income, total_spending, max(0, min(risk_score, 1))


def calculate_base_credit_limit(total_income, total_spending, transactions):
    # Determine the base credit limit using average income and spending
    base_credit_limit = (total_income / max(len(transactions), 1)) * 3
    - (total_spending / max(len(transactions), 1))

    # Ensure the base credit limit is non-negative
    return max(base_credit_limit, 0)
