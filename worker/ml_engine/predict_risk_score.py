import numpy as np

model = None


def predict_risk_score(primary_emotion, intensity, transactions, model):
    """
    Train the model and return the trained model.

    Returns:
    - risk_score
    - final_credit_limit
    """
    if model is None:
        raise Exception("Model not trained. Call train_model() first.")

    # Preprocess inputs
    total_income = sum(
        [trans["amount"] for trans in transactions if trans["amount"] > 0]
    )
    total_spending = sum(
        [abs(trans["amount"]) for trans in transactions if trans["amount"] < 0]
    )
    balance_fluctuation = np.std(
        [trans["balance_after_transaction"] for trans in transactions]
    )

    # Encode primary emotion
    emotion_map = {
        "anger": 0, "anxiety": 1, "stress": 2,
        "happiness": 3, "calm": 4, "neutral": 5,
        "sadness": 6, "fear": 7, "surprise": 8
    }
    emotion_encoded = emotion_map.get(primary_emotion, 5)  # Default neutral if not found

    # Prepare feature vector
    features = np.array([
        total_income, total_spending, balance_fluctuation, intensity, emotion_encoded
    ]).reshape(1, -1)

    risk_score = model.predict(features)[0]
    risk_score = max(0, min(risk_score, 1))  # Ensure risk_score is between 0 and 1
    risk_score = round(risk_score, 2)

    base_credit_limit = calculate_base_credit_limit(
        total_income,
        total_spending,
        transactions
    )
    print(f"Base credit limit calculated: {base_credit_limit}")

    # Adjust the final credit limit based on the risk score
    final_credit_limit = base_credit_limit * (1 - risk_score)
    final_credit_limit = round(final_credit_limit, 2)

    return risk_score, final_credit_limit


def calculate_base_credit_limit(total_income, total_spending, transactions):
    base_credit_limit = (
        total_income / max(len(transactions), 1)) * 3
    - (total_spending / max(len(transactions), 1))

    # Ensure the base credit limit is non-negative
    return max(base_credit_limit, 0)
